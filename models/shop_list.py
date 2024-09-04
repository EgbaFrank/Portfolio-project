"""
Contains the shop_list model implementation
"""
from os import getenv
from .base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, ForeignKey, Table

if getenv("GH_STORAGE_TYPE") == "db":
    shop_list_product = Table(
            'shop_list_product', Base.metadata,
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
        products = relationship(
                'Product',
                secondary='shop_list_product',
                backref='shop_list',
                viewonly=False
                )

    else:
        # Add a status attribute to show list status, e.g. ordered, pending...
        user_id = ""
        total_cost = 0
        product_ids = {}  # {product: quantity}

        @property
        def products(self):
            """getter attribute returns the list of Product instances"""
            from .product import Product
            from models import storage
            products = storage.all("Product")
            return [product for product in products.values()
                    if product.id in self.product_ids.keys()]

        @products.setter
        def add_products(self, value, qty=1):
            """setter attribute manages products I/O operations"""
            from .product import Product
            if not hasattr(self, 'product_ids'):
                self.product_ids = {}
                self.total_cost = 0

            if isinstance(value, Product):
                self.product_ids[value.id] = qty
                self.total_cost += value.price * qty

            elif isinstance(value, dict):
                for product, qty in value.items():
                    if isinstance(product, Product):
                        self.product_ids[product.id] = qty
                        self.total_cost += product.price * qty

    def make_order(self):
        """Create orders from the shopping list grouped by shops."""
        if not self.products:
            return

        from models.order import Order
        orders = []
        shop_products = {}

        # Group products by their shop_id
        for product in self.products:
            if product.shop_id not in shop_products:
                shop_products[product.shop_id] = []
            shop_products[product.shop_id].append(product)

        # Create orders for each shop
        for shop_id, products in shop_products.items():
            total_cost = sum(product.price for product in products)
            new_order = Order(
                status='Pending',
                total_cost=total_cost,
                shop_id=shop_id,
                list_id=self.id,
                user_id=self.user_id
            )
            if getenv("GH_STORAGE_TYPE") == "db":
                new_order.products.extend(products)
            else:
                new_order.products = products
            orders.append(new_order)

        # Save orders to storage
        for order in orders:
            order.save()

        return orders

    def __init__(self, *args, **kwargs):
        """Initialization of instances"""
        super().__init__(*args, **kwargs)
