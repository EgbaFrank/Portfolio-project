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
            Column(
                'quanity', Integer,
                CheckConstraint('quantity > 0'), default=1)
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
        product_ids = []
        product_qty = {}  # {product: quantity}

        @property
        def products(self):
            """getter attribute returns the list of Product instances"""
            from .product import Product
            from models import storage
            products = storage.all("Product")
            return [product for product in products.values()
                    if product.id in self.product_ids]

        @products.setter
        def products(self, value, qty=1):
            """setter attribute manages products I/O operations"""
            from .product import Product
            if 'product_ids' not in self.__dict__:
                self.product_ids = []
                self.product_qty = {}
                self.total_cost = 0

            if isinstance(value, Product):
                self.product_ids.append(value.id)
                self.product_qty[value.id] = 1
                self.total_cost += value.price

            elif isinstance(value, list):
                for product in value:
                    if not isinstance(product, Product):
                        continue
                    if product.id not in self.product_ids:
                        self.product_ids.append(product.id)
                        self.product_qty[product.id] = 1
                        self.total_cost += product.price

    def update_prod_qty(self, product_id, qty):
        """Update the quantity of a specific product in the shop_list."""
        if product_id in self.product_ids and isinstance(qty, int):
            if qty <= 0:
                raise ValueError("Quantity must be a positive integer")

            if getenv("GH_STORAGE_TYPE") == "db":
                stocklist = storage.get_product_qty(self.id, product.id)

                if stocklist:
                    stocklist.quanity = qty
            else:
                self.product_qty[product_id] = qty

            self.total_cost = sum(
                product.price * self.product_qty[product.id] 
                for product in self.products
            )
            return True
        return False

    def send_orders_to_shops(self, orders):
        """Send the created orders to their respective shops."""
        from .shop import Shop
        for order in orders:
            shop = storage.get(Shop, order.shop_id)
            if not shop:
                print(f"Shop with ID {order.shop_id} not found")
                continue
            if getenv("GH_STORAGE_TYPE") == "db":
                shop.orders.append(order)
            else:
                shop.orders = order
            shop.save()

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

        send_orders_to_shops(orders)

    def __init__(self, *args, **kwargs):
        """Initialization of instances"""
        super().__init__(*args, **kwargs)
