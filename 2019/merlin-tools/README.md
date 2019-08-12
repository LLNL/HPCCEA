# Merlin Workflow Tools
Merlin is a LLNL job submission tool that uses the message brokers RabbitMQ and Redis on the backend, and Celery as a task worker. This assists with the installation and securing of those tools. 
Be sure to have all of the scripts, the Puppet manifest, and rabbitmq.config file in the same directory prior to starting the installation process. RabbitMQ messaging will be protected with SSL. 

# Installation
```bash
sudo sh install.sh
```

# Contributors
Sarah Mings, Zeke Morton, Eliana Neurohr
