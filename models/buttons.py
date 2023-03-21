from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Tuple

from .menu import Menu
from .order import Order


class Buttons:
    RESTAURANT_BUTTON = InlineKeyboardButton(
            text='🍔 Restaurantes', callback_data='restaurants'
        )
    ORDERS_BUTTON = InlineKeyboardButton(
            text='📄 Órdenes', callback_data='orders'
        )
    RETURN_BUTTON = InlineKeyboardButton(
            text='🏠 Menú Principal', callback_data='main_menu'
        )
    
    def main(self):
        # Mostrar menú
        return InlineKeyboardMarkup([
                    [self.RESTAURANT_BUTTON], 
                    [self.ORDERS_BUTTON]
                ])
    
    def restaurants(self, restaurants: List) -> InlineKeyboardMarkup:
        keyboard = [[InlineKeyboardButton(text=f'{restaurant["name"]}',
                                 callback_data=f'restaurant_{restaurant["pk"]}')]
                for restaurant in restaurants
                ]
        keyboard.append([self.RETURN_BUTTON])
        
        return InlineKeyboardMarkup(keyboard)
    
    
    def restaurant_menu(self, menu_data) -> Tuple[str, InlineKeyboardMarkup]:
        menu = Menu(menu_data)
        keyboard = []
        
        for m in menu.menu_list:
            for menu_name, products in m.items():
                keyboard.append([InlineKeyboardButton(text=f'👇 {menu_name} 👇', callback_data='_')])
                keyboard.extend([[
                    InlineKeyboardButton(
                        text=f'{product["description"]} ({product["price"]}CUP)',
                        callback_data=f'order_{product["pk"]}_{product["description"]}_{product["price"]}')
                    ] 
                     for product in products]
                )
                
        keyboard.extend([[self.RESTAURANT_BUTTON], [self.ORDERS_BUTTON], [self.RETURN_BUTTON]])
        
        return menu.restaurant_name, InlineKeyboardMarkup(keyboard, 2)
    

    def orders(self, order: Order) -> InlineKeyboardMarkup:
        keyboard = [
            [
                InlineKeyboardButton(
                text=f'{product.name} ({product.price}CUP)',
                callback_data=f'_'
                ),
                InlineKeyboardButton(
                text=f'❌',
                callback_data=f'delete_{product.pk}'
                ),
             ]
            for product in order.products
        ]
        
        if len(order.products) > 0:
            keyboard.append([
                    InlineKeyboardButton(
                        text=f'📤 Enviar orden ({order.total_sale}CUP)',
                        callback_data=f'send'
                    )
                ]) 
        keyboard.extend([
                [InlineKeyboardButton(
                text=f'📬 Órdenes realizadas',
                callback_data=f'server_orders'
                )],
                [self.RESTAURANT_BUTTON], 
                [self.RETURN_BUTTON]
             ])
        
        return InlineKeyboardMarkup(keyboard)
        
    
    def statics(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            [[self.ORDERS_BUTTON], [self.RESTAURANT_BUTTON], [self.RETURN_BUTTON]]
        )
