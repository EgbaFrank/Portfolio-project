"""
Contains place class implementation
"""
from os import getenv
from .base_model import BaseModel, Base
from sqlalchemy import Column, String


class Place(BaseModel, Base):
    """Blueprint for the place model"""
    if getenv("GH_STORAGE_TYPE") == "db":
        from sqlalchemy.orm import relationship
        __tablename__ = "places"

        name = Column(String(128), nullable=False)
        shops = relationship('City',
                             backref='place',
                             order_by='Shop.name',
                             cascade='all, delete-orphan'
                )

    else:
        from . import storage

        name = ""

        @property
        def shops(self):
            """getter for list of shop instances of a place"""
            shops = storage.all("Shop")
            return [shop for shop in shops if shop.place_id == self.id]

    def __init__(self, *args, **kwargs):
        """Initiaalization of instances"""
        super().__init__(*args, **kwargs)
