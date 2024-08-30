"""
Contains shop class implementation
"""
from .base_model import BaseModel


class Shop(BaseModel):
    """Blueprint for shop instances"""
    name = ""
    api_url = ""
    address = ""
    place_id = ""
    product_ids = []

    def __init__(self, *args, **kwargs):
        """Instantiation of objects"""
        super().__init__(*args, **kwargs)
