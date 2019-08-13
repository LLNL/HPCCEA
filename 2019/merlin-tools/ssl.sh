git clone https://github.com/michaelklishin/tls-gen tls-gen
cd tls-gen/basic
make PASSWORD=bunnies
mkdir -p /etc/ssl/rabbitmq
cd result
mv * /etc/ssl/rabbitmq
chcon -t usr_t /etc/ssl/rabbitmq/*
chmod 777  /etc/rabbitmq/rabbitmq.config
cd ../../..
cp rabbitmq.config /tmp/
rm -fr ./tls-gen/
