"""
Contains implementation for the order class
"""
from os import getenv
from .base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer
from sqlalchemy import ForeignKey, Table, CheckConstraint


GH_STORAGE_TYPE = getenv("GH_STORAGE_TYPE")

if GH_STORAGE_TYPE == "db":
    class Order_product(Base):
        """Model for managing product quantities in orders"""
        __tablename__ = "order_products"

        order_id = Column(
                String(60),
                ForeignKey('orders.id',
                           ondelete='CASCADE',
                           onupdate='CASCADE'
                           ),
                primary_key=True
                )

        product_id = Column(
                String(60),
                ForeignKey('products.id',
                           ondelete='CASCADE',
                           onupdate='CASCADE'
                           ),
                primary_key=True
                )

        quantity = Column(
                Integer,
                CheckConstraint('quantity > 0'),
                default=1
                )

        order = relationship(
                'Order',
                back_populates='products'
                )
        product = relationship('Product')

        def __init__(self, order_id, product_id, quantity=1):
            self.order_id = order_id
            self.product_id = product_id
            self.quantity = quantity


class Order(BaseModel, Base):
    if GH_STORAGE_TYPE == "db":
        __tablename__ = "orders"

        status = Column(String(60), nullable=False)
        total_cost = Column(Integer, nullable=False, default=0)
        shop_id = Column(String(60), ForeignKey('shops.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)

        list_id = Column(
                String(60),
                ForeignKey('shop_lists.id'),
                nullable=False
                )

        products = relationship(
                'Order_product',
                back_populates='order',
                cascade='all, delete-orphan'
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
            products = storage.all(Product)
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
        """Initilization of instances"""
        super().__init__(*args, **kwargs)
