"""
Contains the shop_list model implementation
"""
from os import getenv
from .base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, ForeignKey, Table

if getenv("GH_STORAGE_TYPE") == "db":
    shop_list_product = Table('shop_list_product', Base.metadata,
                            Column('shop_list_id', String(60),
                                ForeignKey('shop_lists.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                primary_key=True),
                            Column('product_id', String(60),
                                ForeignKey('products.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                primary_key=True),
                            Column('quanity', Integer, default=1)
                            )

class Shop_list(BaseModel, Base):
    """Blueprints for shop_list model"""
    if getenv("GH_STORAGE_TYPE") == "db":
        __tablename__ = "shop_lists"

        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        total_cost = Column(Integer, nullable=False, default=0)
        products = relationship('Product',
                    secondary='shop_list_product',
                    backref='shop_list',
                    viewonly=False
                )

    else:
        user_id = ""
        total_cost = 0
        product_ids = []  # {product: quantity} consider adding quanity as a product attribute

        @property
        def products(self):
            """getter attribute returns the list of Product instances"""
            from .product import Product
            from models import storage
            products = storage.all("Product")
            return [product for product in products.values() if product.id in self.product_ids]

        @products.setter
        def products(self, value):
            """setter attribute manages products I/O operations"""
            from .product import Product
            self.product_ids = []
            if isinstance(value, Product):
                if value.id not in self.product_ids:
                    self.product_ids.append(value.id)
            elif isinstance(value, list):
                self.product_ids.extend([product.id for product in value
                                if isinstance(product, Product)
                                ])

    def __init__(self, *args, **kwargs):
        """Initialization of instances"""
        super().__init__(*args, **kwargs)
