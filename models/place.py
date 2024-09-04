"""
Contains place class implementation
"""
from os import getenv
from .base_model import BaseModel, Base
from .shop import Shop
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    """Blueprint for the place model"""
    if getenv("GH_STORAGE_TYPE") == "db":
        __tablename__ = "places"

        name = Column(String(128), nullable=False)
        shops = relationship('Shop',
                             backref='place',
                             order_by='Shop.name',
                             cascade='all, delete-orphan'
                             )

    else:

        name = ""
        shop_ids = []

        @property
        def shops(self):
            from . import storage
            from .shop import Shop
            """getter for list of shop instances of a place"""
            shops = storage.all("Shop")
            return [shop for shop in shops.values()
                    if shop.place_id == self.id]

        @shops.setter
        def shops(self, value):
            """setter attribute manages shops I/O operations"""
            from .shop import Shop
            self.shop_ids = []
            if isinstance(value, Shop):
                if value.id not in self.shop_ids:
                    self.shop_ids.append(value.id)
            elif isinstance(value, list):
                self.shop_ids = [
                        shop.id for shop in value
                        if isinstance(shop, Product)
                        ]

    def __init__(self, *args, **kwargs):
        """Initiaalization of instances"""
        super().__init__(*args, **kwargs)
