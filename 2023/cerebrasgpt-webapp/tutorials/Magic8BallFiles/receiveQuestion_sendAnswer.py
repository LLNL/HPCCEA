#Put this file on a compute node (e2 for example)
import pika
import subprocess
import sys
import os
import time
import random  
 
vhost = os.environ.get('RABBITMQ_VHOST')
username = os.environ.get('RABBITMQ_USERNAME')
password = os.environ.get('RABBITMQ_PASSWORD')  
 
credentials = pika.PlainCredentials(username, password)
connection = pika.BlockingConnection(pika.ConnectionParameters('krypton2',5672, vhost, credentials)) #CHANGE NODE NAME
channel = connection.channel()
channel.queue_declare(queue='question')
  
random_list = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]
  
def produce_ans(answer):
    credentials = pika.PlainCredentials(username, password)
    connection2 = pika.BlockingConnection(pika.ConnectionParameters('krypton2',5672, vhost, credentials)) #CHANGE NODE NAME
 
    channel2 = connection2.channel()
    channel2.queue_declare(queue='answer')
    channel2.basic_publish(exchange='', routing_key='answer', body=answer)
    print(" [x] Sent %r" % (answer))
    connection2.close()
  
def callback(ch, method, properties, body):
    print(" [x] Received %r" %(body.decode('UTF-8')))
    random_num = random.randint(0, 19)
    output = random_list[random_num]
    produce_ans("{}".format(output))
  
channel.basic_consume(queue='question', on_message_callback=callback, auto_ack=True)
print("consuming...")
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
