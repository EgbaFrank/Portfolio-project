"""
Contains shop class implementation
"""
from os import getenv
from .base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Shop(BaseModel, Base):
    """Blueprint for shop instances"""
    if getenv("GH_STORAGE_TYPE") == "db":
        __tablename__ = "shops"

        name = Column(String(128), nullable=False)
        api_url = Column(String(128), nullable=False)
        address = Column(String(128), nullable=False)
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)

    else:
        name = ""
        api_url = ""
        address = ""
        place_id = ""
        product_ids = []

    def __init__(self, *args, **kwargs):
        """Instantiation of objects"""
        super().__init__(*args, **kwargs)
