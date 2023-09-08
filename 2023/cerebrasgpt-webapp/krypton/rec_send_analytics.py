from kafka import KafkaConsumer
import json
import pika
import os

#define global variables for use in flask
sentiment = ""

#Get environment variables to protect credentials
vhost = os.environ.get('RABBITMQ_VHOST')
username = os.environ.get('RABBITMQ_USERNAME')
password = os.environ.get('RABBITMQ_PASSWORD')

#After consuming analytics from Kafka, send them to Rabbit so Flask can display them
def rproduce_analytics(msg):
    credentials = pika.PlainCredentials(username, password)
    connection = pika.BlockingConnection(pika.ConnectionParameters('kryptoni',5672,vhost,credentials))
    channel = connection.channel()

    #Declare direct exchange
    channel.queue_declare(queue='analytics')

    #Publish to exchange
    channel.basic_publish(exchange='', routing_key='analytics', body=msg)

    print(" [x] Sent %r" % (msg))
    connection.close()


#Kafka consumer class
class MessageConsumer:
    broker = ""
    topic = ""
    group_id = ""
    logger = None

    def __init__(self, broker, topic, group_id):
        self.broker = broker
        self.topic = topic
        self.group_id = group_id

    #when activates listener, it will consume the analytics + send to rabbit for flask
    def activate_listener(self):
        consumer = KafkaConsumer(bootstrap_servers=self.broker,
                                 group_id=self.group_id,
                                 auto_offset_reset='earliest',
                                 enable_auto_commit=False,
                                 value_deserializer=json.loads)

        consumer.subscribe(self.topic)
        print("consumer is listening....")
        try:
            for message in consumer:
                print("received message = ", message)
                global sentiment
                sentiment = message.value
                #committing message manually after reading from the topic
                consumer.commit()
                #Send to RabbitMQ
                rproduce_analytics(sentiment)
        except KeyboardInterrupt:
            print("Aborted by user...")
        finally:
            consumer.close()

broker = 'kryptoni:9092'
topic1 = "sentiment"
group_id = 'analytics'
kcons = MessageConsumer(broker, topic1, group_id)
while True:
    kcons.activate_listener()


