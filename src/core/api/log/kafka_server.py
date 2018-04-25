#!/usr/bin/python
# -*- coding:utf-8 -*-

from pykafka import KafkaClient

def save2file(msg):
    data_path=""
    filename = "D:\\log-receiver\\tmp\\test.txt"
    with open(filename,'a') as f:
        f.write(msg)

def consumer():
    client = KafkaClient(hosts="localhost:9092")
    print(client.topics)
    topic = client.topics[b'mylog']    #topic名称
    consumer = topic.get_simple_consumer()
    for record in consumer:
        if record is not None:
            valuestr = record.value.decode()   #从bytes转为string类型
            valuedict = eval(valuestr)
            message = valuedict["message"]
            fields = message.split("\u0001")
            for field in fields:
                kv = field.split("\u0002")
                if len(kv) == 2:
                    print(kv[0], '----',kv[1])
                    save2file(kv[1])
            # print('-'*100)



if __name__ == '__main__':
    consumer()