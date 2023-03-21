from typing import List, Dict, Union

class Product:
    def __init__(self, data: List[str]) -> None:
        self.pk: int = int(data[0])
        self.name: str = data[1]
        self.price: float = float(data[2])
      
    @property  
    def to_json(self) -> Dict[str, Union[str, int, float]]:
        return {
            'pk': self.pk,
            'name': self.name,
            'price': self.price
        }