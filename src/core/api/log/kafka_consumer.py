#!/usr/bin/envpython
# _*_coding:utf-8_*_
import json
from kafka import KafkaConsumer
import time
kafka_host = 'localhost'  # kafka服务器地址
kafka_port = 9092  # kafka服务器端口
# 消费topic1的topic,并指定group_id(自定义),多个机器或进程想顺序消费,可以指定同一个group_id,
# 如果想一条消费多次消费,可以换一个group_id,会从头开始消费
# consumer = KafkaConsumer(
#     'mylog',
#     # group_id='my-group',
#     bootstrap_servers=['{kafka_host}:{kafka_port}'.format(kafka_host=kafka_host, kafka_port=kafka_port)]
# )
# for message in consumer:
#     # json读取kafka的消息
#     print(message)
#     # content = json.loads(message.value)
#     # print(content)

def log(str):
        t = time.strftime(r"%Y-%m-%d_%H-%M-%S", time.localtime())
        print("[%s]%s" % (t, str))

log('start consumer')
# 消费192.168.120.11:9092上的world 这个Topic,指定consumer group是consumer-20171017
consumer = KafkaConsumer('mylog', group_id='consumer-20171017', bootstrap_servers=['localhost:9092'])
print(consumer)
for msg in consumer:
    recv = "%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value)
    log(recv)
