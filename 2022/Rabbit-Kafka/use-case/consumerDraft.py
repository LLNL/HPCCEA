'''
Kafka Consumer and RabbitMQ Producer program. Reads from given Kafka topic and publishes task
to appropriate RabbitMQ agent using a specific RabbitMQ routing key for GPU tasks.
'''

from kafka import KafkaConsumer, consumer
from time import sleep
import json, re, pika, os, sys, syslog, argparse

# Command line arguments used to establish a connection with the RabbitMQ Server
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--vhost", help="Vhost to connect to")
parser.add_argument("-u", "--user", help="User to connect with")
parser.add_argument("-p", "--upass", help="User's password")
parser.add_argument("-s", "--server", help="server to connect to")
parser.add_argument("-t", "--topic", help="topic to read from")
args = parser.parse_args()

class MessageConsumer:
    broker = ""
    topic = ""
    group_id = ""
    logger = None

    def __init__(self, broker, topic, group_id):
        self.broker = broker
        self.topic = topic
        self.group_id = group_id

        #initalizing rabbitmq environment 
        credentials = pika.PlainCredentials(args.user, args.upass)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(args.server,5672,args.vhost,credentials))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='workflow', exchange_type='direct')

    def post_to_work_queue(self, message):
        # Searches for a GPU or Large Memory Job posted to syslog. If found, publishes job to correct RabbitMQ queue
        GPUHIT = re.search(r".*TASK: GPU Job Requested", message)
        if GPUHIT:
           self.channel.basic_publish(exchange='workflow',routing_key="GPU",body="Run GPU Job") 
           # routing key directs job to correct queue ('GPU' routing key -> queue for GPU jobs)
        LMHIT =  re.search(r".*TASK: Large Memory Job Requested", message)
        if LMHIT:
           self.channel.basic_publish(exchange='workflow',routing_key="Large Memory",body="Run Large Memory Job")

    def activate_listener(self):
        # Starts Kafka Consumer
        consumer = KafkaConsumer(bootstrap_servers=self.broker,
                                 group_id='my-group',
                                 auto_offset_reset='earliest',
                                 enable_auto_commit=False,
                                 value_deserializer=lambda m: json.loads(m.decode('ascii')))

        consumer.subscribe(self.topic)
        print("consumer is listening....")
        try:
            for message in consumer:
                print("received message = ", message.value)
                self.post_to_work_queue(message.value)
                #committing message manually after reading from the topic
                consumer.commit()
        except KeyboardInterrupt:
            print("Aborted by user...")
        finally:
            consumer.close()

# Run consumer
broker = args.server + ":9092"
topic = args.topic 
group_id = 'consumer-1'

consumer1 = MessageConsumer(broker,topic,group_id)
consumer1.activate_listener()
