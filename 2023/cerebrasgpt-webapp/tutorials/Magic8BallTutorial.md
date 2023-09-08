# Magic 8 Ball Tutorial

## Description

* Create a Flask web application where users can ask yes/no questions and receive an answer back, similar to how a Magic 8 Ball would answer

## RabbitMQ Install

Make sure python3 version on **Management Node** is 3.6 → (python3 --version):

- If not 3.6, use command below to change it
  
```  
update-alternatives --config python3
```
In **e2** of your cluster, complete the following steps:

- Import necessary rpm's

```
rpm --import https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc
rpm --import https://packagecloud.io/rabbitmq/erlang/gpgkey
rpm --import https://packagecloud.io/rabbitmq/rabbitmq-server/gpgkey
```

- Navigate to /etc/yum.repos.d/ and create a new file called rabbitmq.repo with the following content:
  
```
##
## Zero dependency Erlang
##
 
[rabbitmq_erlang]
name=rabbitmq_erlang
baseurl=https://packagecloud.io/rabbitmq/erlang/el/8/$basearch
repo_gpgcheck=1
gpgcheck=1
enabled=1
# PackageCloud's repository key and RabbitMQ package signing key
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
# PackageCloud's repository key and RabbitMQ package signing key
gpgkey=https://packagecloud.io/rabbitmq/erlang/gpgkey
       https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
metadata_expire=300
 
##
## RabbitMQ server
##
[rabbitmq_server]
name=rabbitmq_server
baseurl=https://packagecloud.io/rabbitmq/rabbitmq-server/el/8/$basearch
repo_gpgcheck=1
gpgcheck=0
enabled=1
# PackageCloud's repository key and RabbitMQ package signing key
gpgkey=https://packagecloud.io/rabbitmq/rabbitmq-server/gpgkey
       https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
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
```

Navigate back to the home directory on your compute node/VM and complete these steps:

- Update Yum and enable all repositories:

```
yum update -y
yum -q makecache -y --disablerepo='*' --enablerepo='rabbitmq_erlang' --enablerepo='rabbitmq_server'
```

- Install dependencies + Erlang + RabbitMQ

```
yum install socat logrotate -y
yum install --repo rabbitmq_erlang --repo rabbitmq_server erlang rabbitmq-server -y
```

- Enable and start RabbitMQ:

```
systemctl enable --now rabbitmq-server
systemctl status rabbitmq-server
```

- Create a RabbitMQ user + Virtual Host + Set permissions:
  
```
rabbitmqctl add_user "your_rabbitmq_username"
rabbitmqctl add_vhost "your_vhost_name"
rabbitmqctl set_permissions -p "your_vhost_name" "your_rabbitmq_username" ".*" ".*" ".*"
```

- Repeat the RabbitMQ install for the **management node** of your cluster
  
  - You can use the Ansible script titled rabbit.yml in this repo to automate the install (make sure to change the hosts to "management" in the playbook)

- Add user, vhost, and password to .bashrc as environment variables to keep them protected (do this in both management node and compute node)
  
```
vi .bashrc
 
export RABBITMQ_VHOST='vhost'
export RABBITMQ_USERNAME='your_username'
export RABBITMQ_PASSWORD='your_password'
```
- Exit out of nodes, then re-enter to ensure your new .bashrc configuration is being used

- To make sure your variables saved, run echo $RABBITMQ_USERNAME and make sure you see your username on the command line

**On Management Node (You can skip this part if you did Ansible for management node):**

- If you haven't installed it already, install pip:

```
dnf install -y python3-pip
```

- Install the Pika Python module, which will allow the machine to connect to your RabbitMQ server:

```
python3 -m pip install pika
```

  - `pip install pika (or) pip3 install pika`
    - Debug: If your terminal does not recognize the "pip" or "pip3" commands, but you have installed pip, try running the following command instead:
    - `python3 -m pip install pika`

# Flask App (Continue Here)

- NOTE: The code files you need are already in the Magic8BallFiles folder (Go ahead and clone repo)

- Make a project folder in management node

```
mkdir 8ball
cd 8ball
```

- Create Flask app file: **app.py**

## HTML + CSS FILES

- Inside the 8ball folder, create a new folder called templates and another folder called static

```
mkdir templates
mkdir static
```

- Go into templates and create 2 html files: **index.html and answer.html**

- index.html is where you will submit your questions and answer.html will be the page that displays the answer

- Go into static folder (cd .. | cd static) and create styles.css file: **styles.css**

## RabbitMQ Producer + Consumer

- Create sendQuestion_receiveAnswer.py file (in management node in 8ball folder) to use for producer and consumer in app.py (we are going to import these functions into our flask app): **sendQuestion_receiveAnswer.py**

    - REMINDER: change node name

- Create receiveQuestion_sendAnswer.py in **e2** (can just put it in root for now) to produce your randomly generated answer and send it back to the management node to be displayed on the website: **receiveQuestion_sendAnswer.py**

    - REMINDER: change node name

## View Website on VNC

- Do steps 1-6 on the VNC Tutorial (Do this if you have not set up VNC yet; else just open up VNC as usual)

- Open 3 konsoles (we want to run firefox, app.py, and the RabbitMQ consumer)
  - Konsole 1 (in lgw2-pub)
  ```
  firefox --no-remote
  ```
  - Konsole 2 (in mgmt node - in 8ball folder): 
  ```
  pip3 install flask
  pip3 install pika
  python3 app.py
  ```
  - Konsole 3 (in compute node):
  ```
  pip3 install pika
  python3 receiveQuestion_sendAnswer.py
  ```
  - On Firefox, go to http://CLUSTERNAMEi:8001 (replace CLUSTERNAME with your cluster's name)
  - Optional: to reduce the number of terminals open, you can run Flask app and the RabbitMQ consumer in the background

```
nohup python3 app.py
nohup python3 receiveQuestion_sendAnswer.py
```

## Optional: Kafka Install + Hello World Tutorial

- If there is extra time, feel free to explore the kafka.yml file and set up a hello world pipeline!
- We have an Ansible script that automates the installation of Kafka that you can use too (we recommend installing Kafka manually at least once first, though)
