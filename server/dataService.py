import pandas as pd
import os
import json
import pathlib
import time
from kafka import KafkaConsumer, KafkaProducer
from dataAccess import dataAccessJs
from serverConfig import *

class dataServiceStream():
    ''' Services to handle database requests (In this case, from stream) and dispatch to dbAccess funcitons '''
    def __init__(self):
        self.consumer = KafkaConsumer(
            DATA_REQ_TOPIC,
            bootstrap_servers=[DATA_SERVER_ADDRESS],
            enable_auto_commit=True,
            group_id='my-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    
        self.producer = KafkaProducer(
             bootstrap_servers=[DATA_SERVER_ADDRESS],
             value_serializer=lambda x: json.dumps(x).encode('utf-8'))
    
    def handleMsgLoop(self, db):
        ''' Receive and handle stream messages
        
            All messages to handle:
                {'type':'rm-prd', 'args':(name, num), 'id':n }   --> remove products
                {'type':'get-prd-num', 'time':t}                 --> get each product quantity
                {'type':'get-db', 'time':t}                      --> (dbg)get database info
        '''
        for msg in self.consumer:
            msg = msg.value
            if 'type' not in msg.keys():
                print('rcv invalid msg:', msg)
                continue
            if msg['type'] == 'rm-prd':
                name, num = msg['args']
                rmNum = db.rmProduct(name, num)
                db._dbgData()
                self.producer.send(DATA_RPL_TOPIC, value=
                    {'type':'rpl-rm-prd',
                     'value':rmNum,
                     'id':msg['id'], 
                     'time':time.time()
                    })
            if msg['type'] == 'get-prd-num':
                productsNum = db.getProductsQuantity()
                self.producer.send(DATA_RPL_TOPIC, value=
                    {'type':'rpl-get-prd-num',
                     'value':productsNum,
                     'time':time.time()
                    })
            if msg['type'] == 'get-db':
                data = {'inventory': json.loads(db.inventory.to_json(orient = 'records')),
                        'products': [{name : json.loads(db.products[name].to_json(orient = 'records'))} for name in db.products.keys()]}
                self.producer.send(DATA_RPL_TOPIC, value=
                    {'type':'rpl-get-db',
                     'value':data,
                     'time':time.time()
                    })
                    
if __name__ == '__main__':
    os.chdir(pathlib.Path(__file__).parent.resolve())
    
    db = dataAccessJs(DATA_INV_JS, DATA_PRD_JS)
    # db._dbgData()
    # db.getProductQuantity('Dinning Table')
    # print(db.getProductsQuantity())
    # db.rmProduct('Dinning Table', 1)
    # db._dbgData()
    # db.saveInventory()
    consumer = dataServiceStream()
    consumer.handleMsgLoop(db)

    
    