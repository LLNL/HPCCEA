'''
Kafka reporter program. Reads from given topic and displays sequential list of tasks issued and 
completed.
'''

from kafka import KafkaConsumer, consumer
from kafka import TopicPartition
from time import sleep
import json, argparse

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--server", help="server to connect to")
parser.add_argument("-t", "--topic", help="topic to read from")
args = parser.parse_args()

# Kafka reporter will see to the begining of a topic and print all messages

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
                                 group_id='my-group',
                                 consumer_timeout_ms=60000,
                                 auto_offset_reset='earliest',
                                 enable_auto_commit=False,
                                 value_deserializer=lambda m: json.loads(m.decode('ascii')))

        #consumer.subscribe(self.topic)
        print("consumer is rewinding....")
        topic_partition = TopicPartition(self.topic, 0)
        assigned_topic = [topic_partition]
        consumer.assign(assigned_topic)
        consumer.seek_to_beginning(topic_partition)

        print("consumer is listening....")
        try:
            for message in consumer:
                print("received message = ", message.value)

                #committing message manually after reading from the topic
                consumer.commit()
        except KeyboardInterrupt:
            print("Aborted by user...")
        finally:
            consumer.close()


#Running multiple consumers
broker = args.server + ":9092"
topic = args.topic
group_id = 'reporter-1'

reporter = MessageConsumer(broker,topic,group_id)

reporter.activate_listener()
