#!/usr/bin/python
# -*- coding: UTF-8 -*-
from pykafka import KafkaClient
import logging
# import logging.config
# from ConfigUtil import ConfigUtil
import datetime


class KafkaPython:
    # logging.config.fileConfig("logging.conf")
    # logger = logging.getLogger("msg")
    # logger_data = logging.getLogger("data")

    def __init__(self):
        # self.server = ConfigUtil().get("kafka","kafka_server")
        self.server = "localhost:9092"
        # self.topic = ConfigUtil().get("kafka","topic")
        self.topic = b'mylog'
        # self.group = ConfigUtil().get("kafka","group")
        self.group = b'mylog'
        # self.partition_id = int(ConfigUtil().get("kafka","partition"))
        self.partition_id = 1
        # self.consumer_timeout_ms = int(ConfigUtil().get("kafka","consumer_timeout_ms"))
        self.consumer_timeout_ms = 30
        self.consumer = None
        # self.hosts = ConfigUtil().get("es","hosts")
        self.hosts = "localhost:9200"
        # self.index_name = ConfigUtil().get("es","index_name")
        self.index_name = "mylog"
        # self.type_name = ConfigUtil().get("es","type_name")
        self.type_name = "mylog"


    def getConnect(self):
        client = KafkaClient(self.server)
        topic = client.topics[self.topic]
        p = topic.partitions
        ps={p.get(self.partition_id)}

        self.consumer = topic.get_simple_consumer(
            consumer_group=self.group,
            auto_commit_enable=True,
            consumer_timeout_ms=self.consumer_timeout_ms,
            # num_consumer_fetchers=1,
            # consumer_id='test1',
            partitions=ps
            )
        self.starttime = datetime.datetime.now()


    def beginConsumer(self):
        print("beginConsumer kafka-python")
        imprtEsData = ImportEsData(self.hosts,self.index_name,self.type_name)
        #创建ACTIONS
        count = 0
        ACTIONS = []

        while True:
            endtime = datetime.datetime.now()
            print (endtime - self.starttime).seconds
            for message in self.consumer:
                if message is not None:
                    try:
                        count = count + 1
                        # print(str(message.partition.id)+","+str(message.offset)+","+str(count))
                        # self.logger.info(str(message.partition.id)+","+str(message.offset)+","+str(count))
                        action = {
                            "_index": self.index_name,
                            "_type": self.type_name,
                            "_source": message.value
                        }
                        ACTIONS.append(action)
                        if len(ACTIONS) >= 10000:
                            imprtEsData.set_date(ACTIONS)
                            ACTIONS = []
                            self.consumer.commit_offsets()
                            endtime = datetime.datetime.now()
                            print (endtime - self.starttime).seconds
                            #break
                    except (Exception) as e:
                        # self.consumer.commit_offsets()
                        print(e)
                        self.logger.error(e)
                        self.logger.error(str(message.partition.id)+","+str(message.offset)+","+message.value+"\n")
                        # self.logger_data.error(message.value+"\n")
                    # self.consumer.commit_offsets()


            if len(ACTIONS) > 0:
                self.logger.info("等待时间超过，consumer_timeout_ms，把集合数据插入es")
                imprtEsData.set_date(ACTIONS)
                ACTIONS = []
                self.consumer.commit_offsets()
    def disConnect(self):
        self.consumer.close()


from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
class ImportEsData:

    # logging.config.fileConfig("logging.conf")
    # logger = logging.getLogger("msg")

    def __init__(self,hosts,index,type):
       self.es = Elasticsearch(hosts=hosts.strip(',').split(','), timeout=5000)
       self.index = index
       self.type = type


    def set_date(self,data):
        # 批量处理
        success = bulk(self.es, data, index=self.index, raise_on_error=True)
        self.logger.info(success)



from elasticsearch import Elasticsearch
class ImportEsData:

    # logging.config.fileConfig("logging.conf")
    # logger = logging.getLogger("msg")

    def __init__(self,hosts,index,type):
       self.es = Elasticsearch(hosts=hosts.strip(',').split(','), timeout=5000)
       self.index = index
       self.type = type


    def set_date(self,data):
        # 批量处理
        # es.index(index="test-index",doc_type="test-type",id=42,body={"any":"data","timestamp":datetime.now()})
        self.es.index(index=self.index,doc_type=self.index,body=data)

def kafka2es():
    kp = KafkaPython()
    kp.getConnect()
    kp.beginConsumer()
    # kp.disConnect()


if __name__ == '__main__':
    kafka2es()