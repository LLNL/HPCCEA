'''
This program simulates doing a task in our use case. Once this simulated task is complete, 
a task completion message is then posted to syslog. Binding key is used to determine what types
of jobs the queue will receive
'''

import pika, sys, os, time, syslog, argparse

# Command line arguments used to establish a connection with the RabbitMQ Server
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--vhost", help="Vhost to connect to")
parser.add_argument("-u", "--user", help="User to connect with")
parser.add_argument("-p", "--upass", help="User's password")
parser.add_argument("-b", "--bind", help="binding key/job type")
parser.add_argument("-s", "--server", help="server to connect to")
args = parser.parse_args()

# Establish a connection with the RabbitMQ server
credentials = pika.PlainCredentials(args.user, args.upass)
connection = pika.BlockingConnection(pika.ConnectionParameters(args.server,5672,args.vhost,credentials))
channel = connection.channel()

# Receives messages from the 'workflow' exchange, where all tasks are sent to
channel.exchange_declare(exchange='workflow', exchange_type='direct')

# Declares a queue of random name (queue name irrelavant to program because binding key is used to decide what tasks are sent to the queue)
result = channel.queue_declare(queue='',exclusive=True)
queue_name = result.method.queue
channel.queue_bind(queue=queue_name, exchange='workflow', routing_key=args.bind)

print(' [*] Waiting for jobs. To exit press CTRL+C')

# retrieves and simulates tasks being done
def callback(ch, method, properties, body):
    syslog.openlog(facility=syslog.LOG_LOCAL0)
    body2 = body.decode('UTF-8')
    print(" [x] Received %r" % body2)
    time.sleep(1) # to simulate a task being done
    print(" [x] Task completed")
    syslog.syslog("TASK: %s Job Complete" % args.bind)
    syslog.closelog()

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()                                                                        
