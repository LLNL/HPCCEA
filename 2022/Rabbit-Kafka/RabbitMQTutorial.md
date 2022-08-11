# RabbitMQ Tutorial
## Written by Lindsey Amaro

### Background
RabbitMQ is a message broker, acting as an intermediary service between applications that send and recieve messages. Using RabbitMQ reduces coupling between sender and reciever because, with RabbitMQ handling the transfer and translation of messages, sender and receiver do not directly interact with one another. All messages are stored in queues, which sending and recieving applications can connect to in order to access messages. Sending applications are referred to as producers or publishers, and reciving applications are referred to as consumers or subscribers. Besides the low coupling, RabbitMQ is also beneficial because it allows producers to send their messages in a variety of ways, whether that be directly to a consumer or to an entire group of subscribers. For these and other benefits, RabbitMQ is used by many companies for several types of processes.

**Before beginning this tutorial, ensure that you have 3 AlmaLinux 8 VMs or Compute Nodes that can ping one another set up.** 

### Installing RabbitMQ
On a compute node or VM (do not install on the management node), complete the following steps:
* Import necessary rpms

      rpm --import https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc
      rpm --import https://packagecloud.io/rabbitmq/erlang/gpgkey
      rpm --import https://packagecloud.io/rabbitmq/rabbitmq-server/gpgkey

* Navigate to /etc/yum.repos.d/ and create a new file called rabbitmq.repo with the following content:
 
      ##
      ## Zero dependency Erlang
      ##
      [rabbitmq_erlang]
      name=rabbitmq_erlang
      baseurl=https://packagecloud.io/rabbitmq/erlang/el/8/$basearch
      repo_gpgcheck=1
      gpgcheck=1
      enabled=1
      # PackageClouds repository key and RabbitMQ package signing key
      gpgkey=https://packagecloud.io/rabbitmq/erlang/gpgkey
             https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc
      sslverify=1
      sslcacert=/etc/pki/tls/certs/ca-bundle.crt
      metadata_expire=300

      [rabbitmq_erlang-source]
      name=rabbitmq_erlang-source
      baseurl=https://packagecloud.io/rabbitmq/erlang/el/8/SRPMS
      repo_gpgcheck=1
      gpgcheck=0
      enabled=1
      # PackageClouds repository key and RabbitMQ package signing key
      gpgkey=https://packagecloud.io/rabbitmq/erlang/gpgkey
             https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc
      sslverify=1
      sslcacert=/etc/pki/tls/certs/ca-bundle.crt

      ##
      ## RabbitMQ server
      ##
      [rabbitmq_server]
      name=rabbitmq_server
      baseurl=https://packagecloud.io/rabbitmq/rabbitmq-server/el/8/$basearch
      repo_gpgcheck=1
      gpgcheck=0
      enabled=1
      # PackageClouds repository key and RabbitMQ package signing key
      gpgkey=https://packagecloud.io/rabbitmq/rabbitmq-server/gpgkey
             https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc
      sslverify=1
      sslcacert=/etc/pki/tls/certs/ca-bundle.crt
      metadata_expire=300
      metadata_expire=300

      [rabbitmq_server-source]
      name=rabbitmq_server-source
      baseurl=https://packagecloud.io/rabbitmq/rabbitmq-server/el/8/SRPMS
      repo_gpgcheck=1
      gpgcheck=0
      enabled=1
      gpgkey=https://packagecloud.io/rabbitmq/rabbitmq-server/gpgkey
      sslverify=1
      sslcacert=/etc/pki/tls/certs/ca-bundle.crt
      metadata_expire=300

Navigate back to the home directory on your compute node/VM and complete these steps.
* Update Yum and enable all repositories:

      yum update -y
      yum -q makecache -y --disablerepo='*' --enablerepo='rabbitmq_erlang' --enablerepo='rabbitmq_server'

* Install dependencies

      yum install socat logrotate -y

* Install Erlang and RabbitMQ

      yum install --repo rabbitmq_erlang --repo rabbitmq_server erlang rabbitmq-server -y

* Enable and start RabbitMQ

      systemctl enable --now rabbitmq-server
      systemctl status rabbitmq-server

### Configuring RabbitMQ
On the node/VM where you installed RabbitMQ:
* Create a RabbitMQ user:

      rabbitmqctl add_user "your_rabbitmq_username"

    * Once you type this, it will prompt you to set a password as well
* Create a Virtual Host for this user to connect to:

      rabbitmqctl add_vhost "your_vhost_name"

* Set permissions, so the user you created can access your Virtual Host:

      rabbitmqctl set_permissions -p "your_vhost_name" "your_rabbitmq_username" ".*" ".*" ".*"

### Send and Receive Messages - Hello World Application:
Now, log into a different compute node or VM that you have *not* installed RabbitMQ on.
* If you have not installed it already, install pip:

      dnf install -y python3-pip

* Install the Pika Python module, which will allow the machine to connect to your RabbitMQ server:

      pip install pika or pip3 install pika

    * Debug: If your terminal does not recognize the "pip" or "pip3" commands, but you have installed pip, try running the following command instead: `python3 -m pip install pika`
* Create a file called send.py 
    * On the first line of that file, import pika: `import pika`
    * On the next three lines, as shown below, establish a connection with the RabbitMQ server. Replace `your_rabbitmq_username` and `your_rabbitmq_password` with the RabbitMQ username and password you created in the configuration steps. Replace `server_node` with the name of the node you installed RabbitMQ on (a shortened name or the full name of the node are both acceptable, e.g. 'e3' or 'xenon3'):

          credentials = pika.PlainCredentials('your_rabbitmq_username', 'your_rabbitmq_password')
          connection =  pika.BlockingConnection(pika.ConnectionParameters('server_node', 5672, 'your_vhost', credentials))
          channel = connection.channel()

    * Now, declare a queue your message will go to. You can give the queue any name you like:

          channel.queue_declare(queue='your_queue_name')

    * Publish a message. The routing key is used to deliver the message to the correct queue, and in this example, our routing key will be our queue name.

          channel.basic_publish(exchange='', routing_key='your_queue_name', body="Hello World!")

    * Print a confirmation that your message has been sent, and close the connection between the sender and server: 

          print(" [x] Sent 'Hello World!'")
          connection.close()

    * Example of the complete program:

          import pika

          # establishes a connection with RabbitMQ server
          credentials = pika.PlainCredentials('your_rabbitmq_username', 'your_rabbitmq_password')
          connection = pika.BlockingConnection(pika.ConnectionParameters('server_node',5672,'your_vhost',credentials))
          channel = connection.channel()

          # make sure queue we want to send to exists. If it does not exist, RabbitMQ will just create one
          channel.queue_declare(queue='your_queue_name')

          # send the message
          channel.basic_publish(exchange='', routing_key='test', body='Hello World!')

          print(" [x] Sent 'Hello World!'")
          connection.close()

Now, go to a different compute node or VM, one that does not have RabbitMQ installed and that does not have your send.py file. 
* Install pip (if not already installed) and the Pika Python module, as you did on the node with send.py
* Create a file called receive.py
    * On the first line of the file, import the pika, sys, and os modules: `import pika, sys, os`
    * Delcare the main function: `def main():`
        * Inside that function, establish a connection with the server and delcare the queue you will receive messages from. These 4 lines of code will be exactly the same as they were in send.py. The queue you delcare here must have the same name as the queue you declared in send.py.
        * Still inside the main function, define a callback function, which will print the messages received by the queue:
            
              def callback(ch, method, properties, body):
                  print(" [x] Received %r" %body)

        * Outside of the callback function (but still within the main function), have your receiver begin consuming messages from the queue
        
              channel.basic_consume(queue='your_queue_name', on_message_callback=callback, auto_ack=True)
              print(' [*] Waiting for messages. To exit, press CTRL+C')
              channel.start_consuming()
    * Outside of the main function, write the code that will start your main function:
    
          if __name__=='__main__':
              try:
                  main()
              except KeyboardInterrupt:
                  print('Interrupted')
                  try:
                      sys.exit(0)
                  except SystemExit:
                      os._exit(0)
                      
    * Example of the complete program:
            
          import pika, sys, os
          
          def main()
              credentials = pika.PlainCredentials('your_rabbitmq_username', 'your_rabbitmq_password')
              connection = pika.BlockingConnection(pika.ConnectionParameters('server_node',5672,'your_vhost',credentials))
              channel = connection.channel()
              # must declare queue in both send and receive, since we do not know which will be started first
              channel.queue_declare(queue='test')
              def callback(ch, method, properties, body):
                  print(" [x] Received %r" %body)
                  
              channel.basic_consume(queue='test', on_message_callback=callback, auto_ack=True)
              print(' [*] Waiting for messages. To exit, press CTRL+C')
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

* Now, you are set to run your programs. Open two terminal windows. In one window, go to the node you created receive.py on and run the program ("python3 receive.py"). In the other window, go the node you created send.py on and run the program ("python3 send.py"). Your output should look like the following:
                
      # receive.py - output
      [*] Waiting for messages. To exit, press CTRL+C
      [x] Received 'Hello World!'
    
    The second line of output will appear once you run send.py 

      # send.py - output
      [x] Sent 'Hello World!'

    * Debug: If the second line of your receive.py output looks like `[x] Received b'Hello World!'`, go into your receive.py file and, under the callback function, alter the print statement to say the following:

          print(" [x] Received %r" %(body.decode('UTF-8')))
      
    This should fix the issue.

And that's it! You now have a working RabbitMQ server and Hello World application.
