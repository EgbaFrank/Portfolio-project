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
        image_path = Column(String(128), nullable=False)
        unit = Column(String(60), nullable=False, default="unit")
        shop_id = Column(String(60), ForeignKey('shops.id'), nullable=False)
        category_id = Column(
                String(60),
                ForeignKey('categories.id'),
                nullable=False
                )

    else:
        name = ""
        price = 0
        brand = ""
        image = ""
        unit = ""
        category_id = ""
        shop_id = ""

    def __init__(self, *args, **kwargs):
        """Initialization of instances"""
        super().__init__(*args, **kwargs)
