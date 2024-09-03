"""
Contains implementation for the product class
"""
from os import getenv
from .base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey


class Product(BaseModel, Base):
    """Blueprint for the product class"""
    if getenv("GH_STORAGE_TYPE") == "db":
        __tablename__ = "products"

        name = Column(String(128), nullable=False)
        price = Column(Integer, nullable=False, default=0)
        brand = Column(String(128), nullable=False)
        image = Column(String(128), nullable=False)
        unit = Column(String(60), nullable=False, default="unit")
        category_id = Column(String(60), ForeignKey('categories.id'), nullable=False)

    else:
        name = ""
        price = 0
        brand = ""
        image = ""
        unit = ""
        category_id = ""
        shop_ids = []

        @property
        def shops(self):
            """getter for list of shop instances of a place"""
            from models import storage
            shops = storage.all("Shop")
            return [shop for shop in shops.values() if shop.place_id == self.id]

        @shops.setter
        def shops(self, value):
            """setter attribute manages shops I/O operations"""
            from .shop import Shop
            self.shop_ids = []
            if isinstance(value, Shop):
                if value.id not in self.shop_ids:
                    self.shop_ids.append(value.id)
            elif isinstance(value, list):
                self.shop_ids = [shop.id for shop in value
                                    if isinstance(shop, Shop)]

    def __init__(self, *args, **kwargs):
        """Initialization of instances"""
        super().__init__(*args, **kwargs)
