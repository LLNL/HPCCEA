git clone https://github.com/michaelklishin/tls-gen tls-gen
cd tls-gen/basic
make PASSWORD=bunnies
mkdir -p /etc/ssl/rabbitmq
cd result
mv * /etc/ssl/rabbitmq
chmod 777  /etc/rabbitmq/rabbitmq.config
cd ../../..
rm -fr tls-gen/
