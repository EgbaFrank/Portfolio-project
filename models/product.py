"""
Contains implementation for the product class
"""
from .base_model import BaseModel


class Product(BaseModel):
    """Blueprint for the product class"""
    name = ""
    price = 0
    brand = ""
    image = ""
    unit = ""
    category_id = ""
    shop_ids = []

    def __init__(self, *args, **kwargs):
        """Initialization of instances"""
        super().__init__(*args, **kwargs)
