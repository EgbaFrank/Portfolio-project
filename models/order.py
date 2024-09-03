"""
Contains implementation for the order class
"""
from os import getenv
from .base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, ForeignKey, Table


if getenv("GH_STORAGE_TYPE") == "db":
    order_product = Table('order_product', Base.metadata,
                            Column('order_id', String(60),
                                ForeignKey('orders.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                primary_key=True),
                            Column('product_id', String(60),
                                ForeignKey('products.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                primary_key=True),
                            Column('quanity', Integer, default=1)
                            )

class Order(BaseModel, Base):
    if getenv("GH_STORAGE_TYPE") == "db":
        __tablename__ = "orders"

        status = Column(String(60), nullable=False)
        total_cost = Column(Integer, nullable=False, default=0)
        shop_id = Column(String(60), ForeignKey('shops.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        list_id = Column(String(60), ForeignKey('shop_lists.id'), nullable=False)
        products = relationship(
                'Product',
                secondary="order_product",
                backref='order',
        )

    else:
        shop_id = ""
        list_id = ""
        user_id = ""
        status = ""
        total_cost = 0
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
                self.product_ids.extend([product.id for product in value
                                    if isinstance(product, Product)
                                    ])

    def __init__(self, *args, **kwargs):
        """Initilization of instances"""
        super().__init__(*args, **kwargs)
