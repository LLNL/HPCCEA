from functions import MessageConsumer

broker = 'kryptoni:9092'
group_id = "analytics"

msg_cons = MessageConsumer(broker, "QA", group_id)

while True:
    msg_cons.activate_listener()