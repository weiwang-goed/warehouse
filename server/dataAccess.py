import pandas as pd
import os
import json
import pathlib
import time
from serverConfig import *

class dataAccessJs():
    ''' Funtions to access database (in this case, js files) '''
    def __init__(self, inventoryJs, productJs):
        self.inventory, self.products = {}, {}
        self.inventoryJs, self.productJs = inventoryJs, productJs
        self.loadInventory(inventoryJs)
        self.loadProducts(productJs)
        return
    
    def _dbgData(self):
        ''' debug and show all data '''
        print('-- Inventory dataframe table --')
        inv = self.inventory
        print(inv.head(5))
        # print('-- Inventory article names --')
        # print(list(inv['name']) )
        # print('-- Inventory in-stock statistics --')
        # print(inv['stock'].astype('int32').describe())
        # print('-- Products --')
        # print(self.products.keys())
        return 
 
    def loadInventory(self, path:str):
        ''' load inventory from js '''
        with open(path) as fd:
            d = json.load(fd)
            inv = pd.DataFrame(d['inventory'])
            self.inventory = inv.set_index('art_id')
        return
    
    def _commitInventory(self):
        ''' write loaded inventory back to js '''
        inv = self.inventory.copy()
        inv['art_id'] = inv.index
        invJs = {"inventory": json.loads(inv.astype(str).to_json(orient = 'records'))}
        with open(self.inventoryJs, 'w') as fd:
            json.dump(invJs, fd, indent=2, separators=(',', ': '))
        return
    
    def loadProducts(self, path:str):
        ''' load products menu from js '''
        with open(path) as fd:
            productList = json.load(fd)['products']
            for p in productList:
                self.products[p['name']] = pd.DataFrame(p['contain_articles'])
        return
    
    def getProductQuantity(self, name:str) -> int:
        ''' return maximum quantity of one product from the current inventory
            return 0 if any errors
        '''
        if name not in self.products.keys():
            print('[Warning] Product not found: ', name)
            return 0
        dfPrd = self.products[name]
        try:
            dfInvMatch = self.inventory.loc[dfPrd['art_id']]
        except:
            print('[Warning] Some article category missing in the inventory', list(dfPrd['art_id']) )
            return 0
        
        invArticleStocks = dfInvMatch['stock'].astype(int).to_numpy()
        prdArticleNeeded = dfPrd['amount_of'].astype(int).to_numpy()
        numPerArticle = invArticleStocks/prdArticleNeeded
        print(numPerArticle, int(min(numPerArticle)))
        return int(min(numPerArticle))
    
    def getProductsQuantity(self) -> dict:
        ''' return a dictionary, for each product -> {product : getProductQuantity(product)} '''
        productsQuantity = {}
        for p in self.products.keys():
            productsQuantity[p] = self.getProductQuantity(p)
        return productsQuantity
    
    def rmProduct(self, name:str, num:int):
        ''' remove/sell {num} pieces of product {name}, num < 0 means cancel subscription
        
            1. return number of products successfully sold
            2. update local inventory
        '''
        ## check paramters
        if name not in self.products.keys():
            print('[Warning] Product not found: ', name)
            return 0
        dfPrd = self.products[name]
        try:
            dfInvMatch = self.inventory.loc[dfPrd['art_id']]
        except:
            print('[Warning] Some article category missing in the inventory', list(dfPrd['art_id']) )
            return 0
            
        ## available products to remove
        invArticleStocks = dfInvMatch['stock'].astype(int).to_numpy()
        prdArticleNeeded = dfPrd['amount_of'].astype(int).to_numpy()
        prdNum = int(min(invArticleStocks/prdArticleNeeded))
        rmNum = min(prdNum, num)
        
        ## update inventory dataframe. 
        invArticleStocksNew = invArticleStocks - prdArticleNeeded*rmNum
        self.inventory.loc[dfPrd['art_id'], 'stock'] = invArticleStocksNew
        self._commitInventory()
        
        return rmNum


if __name__ == '__main__':
    os.chdir(pathlib.Path(__file__).parent.resolve())
    
    db = dataAccessJs(DATA_INV_JS, DATA_PRD_JS)
    db._dbgData()
    db.getProductQuantity('Dinning Table')
    print(db.getProductsQuantity())
    db.rmProduct('Dinning Table', 1)
    db._dbgData()
    db.saveInventory()
