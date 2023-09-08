#import subprocess
import pika
import sys
import os
#from textblob import TextBlob

#defining global variables for use in rabbit.py and flask app
received_ans = ""
sentiment = ""

#getting environment variables to protect credential information
vhost = os.environ.get('RABBITMQ_VHOST')
username = os.environ.get('RABBITMQ_USERNAME')
password = os.environ.get('RABBITMQ_PASSWORD')

#rabbitmq produces question to question exchange for consumer to produce answer later
def rproduce_question(msg):
    credentials = pika.PlainCredentials(username, password)
    connection = pika.BlockingConnection(pika.ConnectionParameters('kryptoni',5672, vhost,credentials))
    channel = connection.channel()

    #Declare direct exchange
    channel.queue_declare(queue='question')

    #Publish question to exchange
    channel.basic_publish(exchange='', routing_key='question', body=msg)

    print(" [x] Sent %r" % (msg))
    connection.close()


#consuming answer from LLM that was produced on another node
def rconsume_answer():
    credentials = pika.PlainCredentials(username, password)
    connection = pika.BlockingConnection(pika.ConnectionParameters('kryptoni',5672, vhost,credentials))
    channel2 = connection.channel()

    channel2.queue_declare(queue='answer_time')

    def callback(ch, method, properties, body):
        print(" [x] %r" % (body.decode('UTF-8')))
        global received_ans
        received_ans = body.decode('UTF-8')
        ch.stop_consuming()

    print(' [*] Waiting for logs. To exit press CTRL+C')
    channel2.basic_consume(queue='answer_time', on_message_callback=callback, auto_ack=True)

    try:
        channel2.start_consuming()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    return received_ans

#consume analytics from Kafka from another node for flask to display
def rconsume_analytics():
    credentials = pika.PlainCredentials(username, password)
    connection = pika.BlockingConnection(pika.ConnectionParameters('kryptoni',5672, vhost,credentials))
    channel2 = connection.channel()

    channel2.queue_declare(queue='analytics')

    def callback2(ch, method, properties, body):
        print(" [x] %r" % (body.decode('UTF-8')))
        global sentiment
        sentiment = body.decode('UTF-8')
        ch.stop_consuming()

    print(' [*] Waiting for logs. To exit press CTRL+C')
    channel2.basic_consume(queue='analytics', on_message_callback=callback2, auto_ack=True)

    try:
        channel2.start_consuming()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    return sentiment



