"""
Contains category class implementation
"""
from os import getenv
from sqlalchemy import Column, String
from .base_model import BaseModel, Base
from sqlalchemy.orm import relationship


class Category(BaseModel, Base):
    """Blueprint for the category model"""
    if getenv("GH_STORAGE_TYPE") == "db":
        __tablename__ = "categories"

        name = Column(String(128), nullable=False, unique=True)
        description = Column(String(1024))
        image_path = Column(String(128))
        products = relationship(
                'Product',
                backref='category',
                cascade='all, delete-orphan'
        )

    else:
        name = ""
        description = ""
        image_url = ""
        product_ids = []

        @property
        def products(self):
            """getter attribute returns the list of Product instances"""
            from .product import Product
            from models import storage
            products = storage.all("Product")
            return [product for product in products.values()
                    if product.id in self.product_ids]

        @products.setter
        def products(self, value):
            """setter attribute manages products I/O operations"""
            from .product import Product
            self.product_ids = []
            if isinstance(value, Product):
                if value.id not in self.product_ids:
                    self.product_ids.append(value.id)
            elif isinstance(value, list):
                self.product_ids = [product.id for product in value
                                    if isinstance(product, Product)]

    def __init__(self, *args, **kwargs):
        """Initaialization of instances"""
        super().__init__(*args, **kwargs)
