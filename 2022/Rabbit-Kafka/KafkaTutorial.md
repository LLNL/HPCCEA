# Kafka Tutorial
###### This can be done on compute nodes or vms
---
#####  Prerequisites
- dnf search wget (if not installed, run following: dnf install wget) 
- dnf -y install tar
- dnf -y install java-1.8.0-openjdk java-1.8.0-openjdk-devel
---
######  Download Kafka package into /opt directory 
- wget https://dlcdn.apache.org/kafka/3.2.0/kafka_2.13-3.2.0.tgz -O /opt/kafka_2.13-3.2.0.tgz
######  enter /opt directory and extract it 
- cd /opt
- tar -xvf kafka_2.13-3.2.0.tgz 
- ln -s /opt/kafka_2.13-3.2.0 /opt/kafka
######  ln -s /opt/kafka_2.13-3.2.0 /opt/kafka
- useradd kafka
- chown -R kafka:kafka /opt/kafka*
---
###### Now we can create the zookeeper service. 
Create the file /etc/systemd/system/zookeeper.service with the following content:

 
>>[Unit]
Description=zookeeper
After=syslog.target network.target
[Service]
Type=simple
User=kafka
Group=kafka
ExecStart=/opt/kafka/bin/zookeeper-server-start.sh /opt/kafka/config/zookeeper.properties
ExecStop=/opt/kafka/bin/zookeeper-server-stop.sh
[Install]
WantedBy=multi-user.target

###### Do the same for the Kafka service. 
In a file /etc/systemd/system/kafka.service , add :

>>[Unit]
Description=Apache Kafka
Requires=zookeeper.service
After=zookeeper.service
[Service]
Type=simple
User=kafka
Group=kafka
ExecStart=/opt/kafka/bin/kafka-server-start.sh /opt/kafka/config/server.properties
ExecStop=/opt/kafka/bin/kafka-server-stop.sh
[Install]
WantedBy=multi-user.target
---
######  You need to update zookeeper.properties in /opt/kafka/config/zookeeper.properties with the following line. By default audit logs are disabled
- audit.enable=true 
######  Now reload systemd
- systemctl daemon-reload 
######  Start both services in this order: 
- systemctl start zookeeper 
- systemctl start kafka
######  Both should be active now, you can check with
- systemctl status zookeeper.service 
- systemctl status kafka.service
---
Now let's test it out with an application to send data to and from a topic. We will use python applications to do this
#####  Prerequisites
- dnf install -y python3-pip
- pip3 install kafka-python 
---
######  Create a producer application which uses the KafkaProducer API:
- create a python file called testproducer.py with the following content
- ** NOTE: replace "localhost" with the name of the node (or VM) that you downloaded Kafka on
```
from kafka import KafkaProducer
import json

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
        try:
            future = self.producer.send(self.topic,msg)
            self.producer.flush()
            future.get(timeout=60)
            print("message sent successfully...")
            return {'status_code':200, 'error':None}
        except Exception as ex:
            return ex


broker = 'localhost:9092'
topic = 'test-topic'
message_producer = MessageProducer(broker,topic)

data = {'name':'abc', 'email':'abc@example.com'}
resp = message_producer.send_msg(data)
print(resp)
```
 We also need to create a consumer to read data from the topic using KafkaProducer API
 
- on another node, create a file called testconsumer.py with the following content:
- ** NOTE: replace "localhost" with the name of the node that you downloaded Kafka on

```
from kafka import KafkaConsumer, consumer
from time import sleep
import json


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

        consumer.subscribe(self.topic)
        print("consumer is listening....")
        try:
            for message in consumer:
                print("received message = ", message)

                #committing message manually after reading from the topic
                consumer.commit()
        except KeyboardInterrupt:
            print("Aborted by user...")
        finally:
            consumer.close()


#Running multiple consumers
broker = 'localhost:9092'
topic = 'test-topic'
group_id = 'consumer-1'

consumer1 = MessageConsumer(broker,topic,group_id)
consumer1.activate_listener()

```
---
Finally run these files and verify that Kafka is working on your machine 

- (on the machine with producer) : python3 testproducer.py
- (on the machine with consumer) : python3 testconsumer.py 

Note: code above from tutorial at 
- https://www.tutorialsbuddy.com/kafka-python-producer-example
- https://www.tutorialsbuddy.com/kafka-python-consumer-example
