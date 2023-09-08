#Put this file in management node
import subprocess
import pika
import sys
import os
  
received_ans = "default"
 
vhost = os.environ.get('RABBITMQ_VHOST')
username = os.environ.get('RABBITMQ_USERNAME')
password = os.environ.get('RABBITMQ_PASSWORD')
 
def producer(msg):
    credentials = pika.PlainCredentials(username, password)
    connection = pika.BlockingConnection(pika.ConnectionParameters('krypton2',5672,vhost,credentials)) #CHANGE NODE NAME
    channel = connection.channel()
  
    #Declare direct exchange
    channel.queue_declare(queue='question')
    channel.basic_publish(exchange='', routing_key='question', body=msg)
  
    print(" [x] Sent %r" % (msg))
    connection.close()
  
  
def consumer():    
    credentials = pika.PlainCredentials(username, password)
    connection = pika.BlockingConnection(pika.ConnectionParameters('krypton2',5672,vhost,credentials)) #CHANGE NODE NAME
    channel2 = connection.channel()
  
    channel2.queue_declare(queue='answer')
  
    def callback(ch, method, properties, body):
        print(" [x] %r" % (body.decode('UTF-8')))
        global received_ans
        received_ans = body.decode('UTF-8')
        ch.stop_consuming()
  
    print(' [*] Waiting for logs. To exit press CTRL+C')
    channel2.basic_consume(queue='answer', on_message_callback=callback, auto_ack=True)
     
    try:
        channel2.start_consuming()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
 
    return received_ans
