
# Debugging

## Issues Installing Xturing and Pika on GPU Node

- If having issues installing xturing and pika on GPU, try confirming that the python3 --version is set to Python3.8+ (if the default is set to a lower version, you need to update it)

- after running this command below, select the python version you need (9), and recheck that python3 --version is set to Python3.8+

```
update-alternatives --config python3
```

- Make sure to upgrade pip and any packages that are not updated if you get errors (or downgrade some packages depending)

```
/usr/bin/python3 -m pip install --upgrade pip
```

## Kafka Connectivity Issues w/ Other Node

- If having issues with Kafka connecting between 2 nodes (i.e. kryptoni and lvi), check that your /etc/hosts matches the hostname of where your broker is

```
[09:40 AM] root@kryptoni ~ $ hostname
krypton1
 
[root@lvi ~]# cat /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
 
192.168.59.11 lvi
192.168.59.3 kryptoni krypton1
```

## RabbitMQ Queue Out of Sync

- If RabbitMQ Queue is off by 1, or just not synced properly (answers are being displayed for previous question instead of current question), restart RabbitMQ on that node and re-add your user and vhost

```
rabbitmqctl stop_app
 
rabbitmqctl reset
 
rabbitmqctl start_app
 
rabbitmqctl add_user "user" "pass"
 
rabbitmqctl add_vhost "vhost"
 
rabbitmqctl set_permissions -p "vhost" "user" ".*" ".*" ".*"
```