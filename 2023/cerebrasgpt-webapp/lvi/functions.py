import pika
import time
import random
from kafka import KafkaProducer, KafkaConsumer
import json
from textblob import TextBlob

#getting environment variables to protect credential information
vhost = os.environ.get('RABBITMQ_VHOST')
username = os.environ.get('RABBITMQ_USERNAME')
password = os.environ.get('RABBITMQ_PASSWORD')

# RabbitMQ producer that sends the answer produced by CerebrasGPT and response time to kryptoni
def rproducer2(answer_time):
    credentials = pika.PlainCredentials(username, password)
    connection2 = pika.BlockingConnection(pika.ConnectionParameters('kryptoni',5672,vhost,credentials))
    channel2 = connection2.channel()
    channel2.queue_declare(queue='answer_time')
    channel2.basic_publish(exchange='', routing_key='answer_time', body=answer_time)
    print(" [x] Sent %r" % (answer_time))
    connection2.close()

# General Kafka producer class and functions
class MessageProducer:
    broker = ""
    topic = ""
    producer = None

    def __init__(self, broker, topic):
        self.broker = broker
        self.topic = topic
        self.producer = KafkaProducer(bootstrap_servers=self.broker,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        acks='all',
        retries = 3)

    def send_msg(self, msg):
        print("sending message...")
        print(msg)
        try:
            future = self.producer.send(self.topic,msg)
            self.producer.flush()
            future.get(timeout=60)
            print("message sent successfully...")
            return {'status_code':200, 'error':None}
        except Exception as ex:
            return ex

# Function that analyzes the the sentiment of the question and answer
def analyze_msg(msg):
    elements = msg.split(" : ")
    question = TextBlob(elements[0])
    answer = TextBlob(elements[1])
    qsentiment = question.sentiment
    asentiment = answer.sentiment
    sentiment = str(qsentiment) + " : " + str(asentiment)
    return str(sentiment)

#Kafka producer that sends the sentiment of the question and answer to the topic "sentiment"
kproducer_sentiment = MessageProducer("kryptoni:9092", "sentiment")

# Kafka consumer that sends the sentiment of the question and answer to kryptoni
class MessageConsumer:
    broker = ""
    topic = ""
    group_id = ""
    logger = None

    def __init__(self, broker, topic, group_id):
        self.broker = broker
        self.topic = topic
        self.group_id = group_id

    def activate_listener(self):
        consumer = KafkaConsumer(bootstrap_servers=self.broker,
                                 group_id=self.group_id,
                                 auto_offset_reset='earliest',
                                 enable_auto_commit=False,
                                 value_deserializer=lambda m: json.loads(m.decode('ascii')))

        consumer.subscribe(self.topic)
        print("consumer is listening....")
        try:
            for message in consumer:
                print("received message = ", message.value)

                #Analyzing sentiment of question and answer
                kproducer_sentiment.send_msg(analyze_msg(message.value))

                #committing message manually after reading from the topic
                consumer.commit()

        except KeyboardInterrupt:
            print("Aborted by user...")
        finally:
            consumer.close()
