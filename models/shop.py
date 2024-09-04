"""
Contains shop class implementation
"""
from os import getenv
from .base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey


class Shop(BaseModel, Base):
    """Blueprint for shop instances"""
    if getenv("GH_STORAGE_TYPE") == "db":
        __tablename__ = "shops"

        name = Column(String(128), nullable=False)
        api_url = Column(String(128))
        address = Column(String(128))
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        orders = relationship(
                'Order',
                backref='shop',
                cascade='all, delete-orphan'
        )

        products = relationship(
                    'Product',
                    backref='shop',
                    cascade='all, delete-orphan'
                )
    else:
        name = ""
        api_url = ""
        address = ""
        place_id = ""
        order_ids = []
        product_ids = []

        @property
        def orders(self):
            """getter attribute returns the list of Order instances"""
            from .order import Order
            from models import storage
            orders = storage.all("Order")
            return [order for order in orders.values()
                    if order.id in self.order_ids]

        @orders.setter
        def orders(self, value):
            """setter attribute manages orders I/O operations"""
            from .order import Order
            self.order_ids = []
            if isinstance(value, Order):
                if value.id not in self.order_ids:
                    self.order_ids.append(value.id)
                elif isinstance(value, list):
                    self.order_ids.extend([
                        order.id for order in value
                        if isinstance(order, Order)
                        ])

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
                self.product_ids.extend([
                    product.id for product in value
                    if isinstance(product, Product)
                    ])

    def __init__(self, *args, **kwargs):
        """Instantiation of objects"""
        super().__init__(*args, **kwargs)
