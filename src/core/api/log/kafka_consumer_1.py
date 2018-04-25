from pykafka import KafkaClient
import logging
#
client = KafkaClient(hosts="localhost:9092")

topic = client.topics[b'mylog']

balanced_consumer= topic.get_balanced_consumer(
    consumer_group=b'mylog',
    auto_commit_enable=True,
#    reset_offset_on_start=True,
    zookeeper_connect='localhost:3274'
)
def save2file(msg):
    # data_path=""
    filename = "D:\\log-receiver\\tmp\\test.txt"
    with open(filename,'a') as f:
        f.write(msg)

def save2es(msg):
    '''
    将kafka读出来的数据保存到es里面
    :param msg: kafka读出来的信息
    :return: None
    '''
    pass

for message in balanced_consumer:
    if message is not None:
        save2file(message.value.decode()+"\n")
        # print(message.offset, message.value)

#
# from pykafka import KafkaClient
# client = KafkaClient(hosts="localhost:9092")
# #print client.brokers
# for n in client.brokers:
#     host = client.brokers[n].host
#     port = client.brokers[n].port
#     id = client.brokers[n].id
#     print("host=%s | port=%s | broker.id=%s " %(host,port,id))