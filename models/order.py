import json

from random import randint
from typing import Dict, List
from .client import Client
from .product import Product


class Order:
    def __init__(self, client: Client) -> None:
        self.id = 'og-'
        self.client_id = client.pk
        self.chat_id = client.chat_id
        self.products: List[Product] = []
        self.created = self.get_or_create()
        
        
    @property 
    def to_send(self) -> Dict:
        return {
                'order_id': self.id,
                'client': self.client_id,
                'products': [product.pk for product in self.products]
            }
    
    @property   
    def to_json(self) -> Dict:
        return {
                'id': self.id,
                'client_id': self.client_id,
                'chat_id': self.chat_id,
                'products': self.products
            }
    
    def read(self):
        with open('db/orders.json', 'r', encoding='utf-8') as file:
            orders: Dict = json.load(file)
            
        order_data = orders[str(self.client_id)]
        
        self.id = order_data['id']
        self.chat_id = order_data['chat_id']
        self.products = []
        
        for product in order_data['products']:
            self.products.append(
                Product([str(value) for value in product.values()])
                )
            
        return self
    
    
    def get_or_create(self):
        with open('db/orders.json', 'r', encoding='utf-8') as file:
            orders: Dict = json.load(file)
            
        order_data = orders.get(str(self.client_id), None)
        
        if not order_data:
            self.id = f'{self.id}{randint(1000, 9999)}'
            orders[str(self.client_id)] = self.to_json

            with open('db/orders.json', 'w', encoding='utf-8') as file:
                json.dump(orders, file, indent=4)
                
            return True
        
        return False
    
    
    def delete(self) -> None:
        with open('db/orders.json', 'r', encoding='utf-8') as file:
            orders: Dict = json.load(file)      
        order_data = orders.get(str(self.client_id), None)
        
        if order_data:
            orders.pop(str(self.client_id))
            with open('db/orders.json', 'w', encoding='utf-8') as file:
                json.dump(orders, file, indent=4)
                
        return
    
        
    def add_product(self, product: Product):
        self.products.append(product)
        
        with open('db/orders.json', 'r', encoding='utf-8') as file:
            orders: Dict = json.load(file)
            
        orders[(str(self.client_id))]['products'].append(product.to_json)
        
        with open('db/orders.json', 'w', encoding='utf-8') as file:
                json.dump(orders, file, indent=4)
                
                
    def delete_product(self, product_id: int):
        with open('db/orders.json', 'r', encoding='utf-8') as file:
            orders: Dict = json.load(file)
        
        order_data = orders[(str(self.client_id))]
            
        for index, product in enumerate(order_data['products']):
            if product['pk'] == product_id:
                order_data['products'].pop(index)
                orders[(str(self.client_id))] = order_data
                self.products = list(filter(
                    lambda product: product.pk != product_id, self.products
                    ))

        with open('db/orders.json', 'w', encoding='utf-8') as file:
            json.dump(orders, file, indent=4)
                
        
    @staticmethod
    def check_db():
        try:
            with open('db/orders.json', 'r', encoding='utf-8') as file:
                pass
        except FileNotFoundError:
            import os
            
            os.mkdir('db')
            
            with open('db/orders.json', 'w', encoding='utf-8') as file:
                json.dump({}, file, indent=4)
                
    @property
    def total_sale(self) -> float:
        return sum([product.price for product in self.products])
    