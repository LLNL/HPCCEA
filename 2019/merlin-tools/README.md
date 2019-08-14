# Merlin Workflow Tools
Merlin is a LLNL job submission tool that uses the message brokers RabbitMQ and Redis on the backend, and Celery as a task worker. This assists with the installation and securing of those tools. RabbitMQ messaging will be protected with SSL. 

Choose to either use Puppet to configure Redis, RabbitMQ, and Celery, or run separate dockers for RabbitMQ and Redis. 

# Contributors
Sarah Mings, Zeke Morton, Eliana Neurohr
