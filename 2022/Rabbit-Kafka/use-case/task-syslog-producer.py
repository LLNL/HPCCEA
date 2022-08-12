'''
Kafka Producer for use case. Reads from syslog and publishes task messages to the 
given Kafka topic.
'''

#!/usr/bin/python3

from kafka import KafkaProducer
from sh import tail
import re
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--server", help="server to connect to")
parser.add_argument("-t", "--topic", help="topic to read from")
args = parser.parse_args()

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

#message format 
    def send_msg(self, msg):
        print("sending message... %s" % (msg) )
        try:
            future = self.producer.send(self.topic,msg)
            self.producer.flush()
            future.get(timeout=60)
            print("message sent successfully...")
            return {'status_code':200, 'error':None}
        except Exception as ex:
            return ex

def main():
   broker = args.server + ":9092"
   topic = args.topic
   message_producer = MessageProducer(broker,topic)

#iterates through each new message in syslog 
#if message is task message, send message to topic
#prints every new message in syslog 

   for line in tail("-f", "/var/log/messages", _iter=True):
      print(line, end='')
      hit = re.search(r".*TASK:.*", line)
      if hit:
         print('HIT: ', hit.group())
         resp = message_producer.send_msg(hit.group())
         print(resp)
      

if __name__ == "__main__":
    main()

