"""
Contains implementation for the order class
"""
from .base_model import BaseModel


class Order(BaseModel):
    shop_id = ""
    list_id = ""
    status = ""
    total_cost = 0
    items = [] # product_ids

    def __init__(self, *args, **kwargs):
        """Initilization of instances"""
        super().__init__(*args, **kwargs)
