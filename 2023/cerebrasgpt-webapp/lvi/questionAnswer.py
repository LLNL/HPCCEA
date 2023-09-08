import pika
import subprocess
import sys
import os
import time
import random
from xturing.datasets.instruction_dataset import InstructionDataset
from xturing.models.base import BaseModel
from kafka import KafkaProducer
import json
from functions import rproducer2, MessageProducer
import datetime

#Get RabbitMQ credentials from .bashrc file
vhost = os.environ.get('RABBITMQ_VHOST')
username = os.environ.get('RABBITMQ_USERNAME')
password = os.environ.get('RABBITMQ_PASSWORD')

#RabbitMQ - Create a channel
credentials = pika.PlainCredentials(username, password)
connection = pika.BlockingConnection(pika.ConnectionParameters('kryptoni',5672,vhost,credentials))
channel = connection.channel()
channel.queue_declare(queue='question')

#Kafka - declare a producer and broker
broker = 'kryptoni:9092'
msg_prod = MessageProducer(broker, "QA")

# Load a fine-tuned model (CerebrasGPT)
finetuned_model = BaseModel.load("./cerebras-1.3B-alpaca-tuned")

def callback(ch, method, properties, body):
    print(" [x] Received %r" %(body.decode('UTF-8')))
    question = body.decode('UTF-8')

    #Getting the response time (starting timer when question is received)
    start_time = int(datetime.datetime.now().timestamp())

    #Generating answer from LLM
    output = finetuned_model.generate(texts=[question])
    end_time = int(datetime.datetime.now().timestamp())

    #Reformatting output
    output = "{}".format(output)[2:-2]
    total_time = end_time - start_time

    #Send question and answer to Kafka for analytics
    combinedQA = str(question) + " : " + output
    msg_prod.send_msg(combinedQA)

    #Send answer and time back to kryptoni
    rproducer2(output + " : " + str(total_time))

channel.basic_consume(queue='question', on_message_callback=callback, auto_ack=True)
channel.start_consuming()

if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
