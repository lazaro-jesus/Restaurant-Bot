from typing import Dict, List
from aiohttp import ClientSession


CLIENTS_SERVICE_URL = 'http://menu.pythonanywhere.com/api/v1/'
CLIENTS_EXISTS = CLIENTS_SERVICE_URL + 'clientexist/{}/'
CLIENTS_CREATE = CLIENTS_SERVICE_URL + 'createclient/'

RESTAURANTS_GET = 'http://menu.pythonanywhere.com/api/v1/listrestaurants'
RESTAURANTS_MENU_GET = 'http://menu.pythonanywhere.com/api/v1/listmenu/{}/'

ORDERS_GET = 'http://menu.pythonanywhere.com/api/v1/listorders/{}/'
ORDERS_CREATE = 'http://menu.pythonanywhere.com/api/v1/createorder/'


async def client_exists(chat_id: int) -> Dict:
    async with ClientSession() as session:
        async with session.get(CLIENTS_EXISTS.format(chat_id)) as response:
            data = await response.json()
            if data['exist']:
                return data['client']
            return {}


async def client_create(body: Dict) -> Dict:
    async with ClientSession() as session:
        async with session.post(CLIENTS_CREATE, json=body) as response:
            if response.status == 201:
                profile = await response.json()
                return profile
            return {}


async def restaurant_list() -> List:
    async with ClientSession() as session:
        async with session.get(RESTAURANTS_GET) as response:
            data = await response.json()
            return data['results']


async def restaurant_menu(restaurant_id: int) -> Dict:
    async with ClientSession() as session:
        async with session.get(RESTAURANTS_MENU_GET.format(restaurant_id)) as response:
            data = await response.json()
            return data['results']


async def order_list(client_id: int) -> Dict:
    async with ClientSession() as session:
        async with session.get(ORDERS_GET.format(client_id)) as response:
            data = await response.json()
            return data['results']
        
        
async def order_create(body: Dict) -> Dict:
    async with ClientSession() as session:
        async with session.post(ORDERS_CREATE, json=body) as response:
            if response.status == 201:
                order = await response.json()
                return order
            return {}
