#!/bin/bash

rabbitmqctl delete_user guest
rabbitmqctl add_vhost /Rabbit
rabbitmqctl add_user Rabbit passw0rd
rabbitmqctl set_permissions -p /Rabbit Rabbit ".*" ".*" ".*"
