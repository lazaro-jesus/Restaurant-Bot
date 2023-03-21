from typing import List, Dict


class Menu:
    def __init__(self, menu: List[Dict]) -> None:
        self.restaurant_id = menu[0]['restaurant']['pk']
        self.restaurant_name = menu[0]['restaurant']['name']
        self.menu_list: List[Dict] = [{m['name']: m['products']} for m in menu]
