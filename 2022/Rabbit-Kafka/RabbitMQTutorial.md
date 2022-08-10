# RabbitMQ Tutorial

### Background
RabbitMQ is a message broker, acting as an intermediary service between applications that send and recieve messages. Using RabbitMQ reduces coupling between sender and reciever because, with RabbitMQ handling the transfer and translation of messages, sender and receiver do not directly interact with one another. All messages are stored in queues, which sending and recieving applications can connect to in order to access messages. Sending applications are referred to as producers or publishers, and reciving applications are referred to as consumers or subscribers. Besides the low coupling, RabbitMQ is also beneficial because it allows producers to send their messages in a variety of ways, whether that be directly to a consumer or to an entire group of subscribers. For these and other benefits, RabbitMQ is used by many companies for several types of processes.

### Installing RabbitMQ
On a compute node or VM (do not install on the management node), complete the following steps:
* Import necessary rpms
    * `rpm --import https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc`
    * `rpm --import https://packagecloud.io/rabbitmq/erlang/gpgkey`
    * `rpm --import https://packagecloud.io/rabbitmq/rabbitmq-server/gpgkey`
* Navigate to /etc/yum.repos.d/ and create a new file called rabbitmq.repo with the following content:
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
```

Navigate back to the home directory on your compute node/VM and complete these steps.
* Update Yum and enable all repositories:
    * `yum update -y`
    * `yum -q makecache -y --disablerepo='*' --enablerepo='rabbitmq_erlang' --enablerepo='rabbitmq_server'`
* Install dependencies
    * `yum install socat logrotate -y` 
* Install Erlang and RabbitMQ
    * `yum install --repo rabbitmq_erlang --repo rabbitmq_server erlang rabbitmq-server -y`
* Enable and start RabbitMQ
    * `systemctl enable --now rabbitmq-server`
    * `systemctl status rabbitmq-server`

### Configuring RabbitMQ
On the node/VM where you installed RabbitMQ:
* Create a RabbitMQ user:
    * `rabbitmqctl add_user "your_rabbitmq_username"`
    * Once you type this, it will prompt you to set a password as well
* Create a Virtual Host for this user to connect to:
    * `rabbitmqctl add_vhost "your_vhost_name"`
* Set permissions, so the user you created can access your Virtual Host:
    * `rabbitmqctl set_permissions -p "your_vhost_name" "your_rabbitmq_username" ".*" ".*" ".*"`


