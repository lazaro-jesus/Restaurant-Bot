import json

from typing import Optional, Dict
from telebot.types import Message


class Client:
    def __init__(self, message: Message):
        self.pk: int = -1
        self.chat_id: int = message.chat.id
        self.first_name: str = message.from_user.first_name
        self.username: Optional[str] = message.from_user.username
        self.language_code: str = message.from_user.language_code
        self.created = self.get_or_create()
    

    def get_pk(self):
        with open('db/clients.json', 'r', encoding='utf-8') as file:
            clients: Dict = json.load(file)
        self.pk = clients[str(self.chat_id)]['pk']
        
        return self
        
    @property
    def to_json(self) -> Dict:
        return {
                "pk": self.pk,
                "first_name_telegram": self.first_name,
                "username_telegram": self.username,
                "chatID": str(self.chat_id),
                "language_code": self.language_code
            }
        
        
    def get_or_create(self):
        with open('db/clients.json', 'r', encoding='utf-8') as file:
            clients: Dict = json.load(file)
            
        client_data = clients.get(str(self.chat_id), None)
        
        if not client_data:
            clients[str(self.chat_id)] = self.to_json

            with open('db/clients.json', 'w', encoding='utf-8') as file:
                json.dump(clients, file, indent=4)
                
            return True
        
        return False
    
    
    def update(self, data) -> None:
        self.pk = data['pk']
        self.chat_id = data['chatID']
        self.first_name = data['first_name_telegram']
        self.username = data['username_telegram']
        self.language_code = data['language_code']
        
        with open('db/clients.json', 'r', encoding='utf-8') as file:
            clients = json.load(file)
            
        clients[self.chat_id] = self.to_json
        
        with open('db/clients.json', 'w', encoding='utf-8') as file:
                json.dump(clients, file, indent=4)
        


    @staticmethod
    def check_db():
        try:
            with open('db/clients.json', 'r', encoding='utf-8') as file:
                pass
        except FileNotFoundError:
            with open('db/clients.json', 'w', encoding='utf-8') as file:
                json.dump({}, file, indent=4)