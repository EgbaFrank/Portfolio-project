"""
Contains the shop_list model implementation
"""
from .base_model import BaseModel


class Shop_list(BaseModel):
    """Blueprints for shop_list model"""
    user_id = ""
    total_cost = 0
    product_ids = {} # {product: quantity}

    def __init__(self, *args, **kwargs):
        """Initialization of instances"""
        super().__init__(*args, **kwargs)
