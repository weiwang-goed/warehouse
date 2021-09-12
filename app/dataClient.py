import pandas as pd
import os
import json
import pathlib
from kafka import KafkaProducer,KafkaConsumer
from time import sleep
import time
import random

DATA_SERVER_ADDRESS = "0.0.0.0:9092" ## (ip:port) opened to access data from network 
DATA_REQ_TOPIC = 'inventory-reqeusts'
DATA_RPL_TOPIC = 'inventory-reply'

class dataReqSync():
    ''' Test dataService '''
    def __init__(self):
        self.consumer = KafkaConsumer(
            DATA_RPL_TOPIC,
            bootstrap_servers=[DATA_SERVER_ADDRESS],
            enable_auto_commit=True,
            auto_offset_reset='latest',
            group_id='my-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')))
        self.producer = KafkaProducer(
             bootstrap_servers=[DATA_SERVER_ADDRESS],
             value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )

    def rmProduct(self, name, num):
        id = random.randint(0,1e5) ## should be unique id for each test
        data = {'type':'rm-prd', 'args':(name, num), 'id':id }
        self.producer.send(DATA_REQ_TOPIC, value=data)
        for msg in self.consumer: ## look for our reply-event with the same id
            msg = msg.value
            print('[msg] :', msg)
            if 'type' not in msg.keys():
                continue
            if msg['type'] == 'rpl-rm-prd' and id == msg['id']:
                return msg['value']
    
    def getProductNum(self):
        t = time.time() ## should be unique id for each test
        data = {'type':'get-prd-num', 'time':time.time() }
        self.producer.send(DATA_REQ_TOPIC, value=data)
        for msg in self.consumer: ## look for our reply-event with newest timestamp
            msg = msg.value
            print('[msg] :', msg)
            if 'type' not in msg.keys():
                continue
            if msg['type'] == 'rpl-get-prd-num':
                if msg['time'] < t:
                    print('Oops, the reply is older than our last request?')
                return msg['value']
    
    def getDb(self):
        t = time.time() ## should be unique id for each test
        data = {'type':'get-db', 'time':time.time() }
        self.producer.send(DATA_REQ_TOPIC, value=data)
        for msg in self.consumer: ## look for our reply-event with newest timestamp
            msg = msg.value
            print('[msg] :', msg)
            if 'type' not in msg.keys():
                continue
            if msg['type'] == 'rpl-get-db':
                if msg['time'] < t:
                    print('Oops, the reply is older than our last request?')
                return msg['value']
                

if __name__ == '__main__':
    tester = dataReqSync()
    tester.rmProduct("Dinning Table", 2)
    tester.getProductNum()
    # tester.getDb()
    # tester.consumer.commit()