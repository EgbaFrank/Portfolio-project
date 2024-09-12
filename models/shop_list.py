"""
Contains the shop_list model implementation
"""
from os import getenv
from .base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer
from sqlalchemy import ForeignKey, Table, CheckConstraint

GH_STORAGE_TYPE = getenv("GH_STORAGE_TYPE")

if GH_STORAGE_TYPE == "db":
    class Shop_list_product(Base):
        """Model for managing product quantities in shop lists"""
        __tablename__ = "shop_list_products"

        shop_list_id = Column(
                String(60),
                ForeignKey('shop_lists.id',
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
        shop_list = relationship(
                'Shop_list',
                back_populates='products'
                )
        product = relationship('Product')

        def __init__(self, shop_list_id, product_id, quantity=1):
            self.shop_list_id = shop_list_id
            self.product_id = product_id
            self.quantity = quantity


class Shop_list(BaseModel, Base):
    """Blueprints for shop_list model"""
    if GH_STORAGE_TYPE == "db":
        __tablename__ = "shop_lists"

        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        total_cost = Column(Integer, nullable=False, default=0)
        products = relationship(
                'Shop_list_product',
                back_populates='shop_list',
                cascade='all, delete-orphan'
                )

        orders = relationship(
                'Order',
                backref='shop_list',
                cascade='all, delete-orphan'
        )

    else:
        # Add a status attribute to show list status, e.g. ordered, pending...
        # this would also allow for prevention of products deletion after ordering

        user_id = ""
        total_cost = 0
        order_ids = []
        product_ids = []
        product_qty = {}  # {product: quantity}

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
            if 'product_ids' not in self.__dict__:
                self.product_ids = []
                self.product_qty = {}
                self.total_cost = 0

            if isinstance(value, Product):
                self.product_ids.append(value.id)
                self.product_qty[value.id] = 1
                self.total_cost += value.price

            if isinstance(value, tuple):
                product, qty = value
                if isinstance(product, Product):
                    self.product_ids.append(product.id)
                    self.product_qty[product.id] = qty
                    self.total_cost += product.price

            elif isinstance(value, list):
                for product in value:
                    if not isinstance(product, Product):
                        continue
                    if product.id not in self.product_ids:
                        self.product_ids.append(product.id)
                        self.product_qty[product.id] = qty
                        self.total_cost += product.price

    def update_total_cost(self):
        """Updates the total cost"""
        from models import storage
        if GH_STORAGE_TYPE == "db":
            product_data = storage.get_product_data(self.id)
            self.total_cost = sum(
                price * quantity for price, quantity in product_data
            )
        else:
            self.total_cost = sum(
                product.price * self.product_qty.get(product.id, 0)
                for product in self.products
            )
        storage.save()

    def set_product_qty(self, product_id, qty=1):
        """Set the quantity of a product in a shop list"""
        from models import storage

        if not isinstance(qty, int) or qty <= 0:
            raise ValueError("Quantity must be a positive integer")

        if GH_STORAGE_TYPE == "db":
            # Retrieve association if it exists
            product = storage.get_product(self.id, product_id)

            # If the association does not exist, create it
            if not product:
                product = Shop_list_product(
                    shop_list_id=self.id,
                    product_id=product_id,
                    quantity=qty
                )
                storage.new(product)

            else:
                # Update the quantity if the association already exists
                product.quantity = qty
        else:
            if product_id in self.product_ids:
                self.product_qty[product_id] = qty
            else:
                from models.product import Product
                product = storage.get(Product, product_id)

                if not product:
                    raise ValueError("Product id not found")
                self.products = product, qty

        self.save()
        self.update_total_cost()

    def send_orders_to_shops(self, orders):
        """Send the created orders to their respective shops."""
        from .shop import Shop
        from models import storage
        for order in orders:
            shop = storage.get(Shop, order.shop_id)
            if not shop:
                print(f"Shop with ID {order.shop_id} not found")
                continue
            if GH_STORAGE_TYPE != "db":
                shop.orders = order
            shop.save()

    def link_orders_to_user(self, orders):
        """Link the created orders to their respective users"""
        from .user import User
        from models import storage
        if orders:
            user = storage.get(User, orders[0].user_id)
            if not user:
                print(f"User with ID {order.user_id} not found")
                return
            if GH_STORAGE_TYPE != "db":
                user.orders = orders
                user.save()

    def make_order(self):
        """Create orders from the shopping list grouped by shops."""
        if not self.products:
            return

        from models.order import Order
        orders = []
        shop_products = {}

        # Group products by their shop_id

        # linklist works as a product on FileStorage
        # and as a shop_list_product association instance
        # on db storage
        for listlink in self.products:
            if GH_STORAGE_TYPE == "db":
                shop_id = listlink.product.shop_id
            else:
                shop_id = listlink.shop_id
            if shop_id not in shop_products:
                shop_products[shop_id] = []
            shop_products[shop_id].append(listlink)

        # Create orders for each shop
        for shop_id, listlinks in shop_products.items():
            if GH_STORAGE_TYPE == "db":
                total_cost = sum(
                        listlink.product.price * listlink.quantity
                        for listlink in listlinks
                        )
            else:
                total_cost = sum(
                        listlink.price * self.product_qty.get(listlink.id, 0)
                        for listlink in listlinks
                        )

            new_order = Order(
                status='Pending',
                total_cost=total_cost,
                shop_id=shop_id,
                list_id=self.id,
                user_id=self.user_id
            )
            new_order.save()
            if GH_STORAGE_TYPE == "db":
                from models import storage
                from models.order import Order_product
                for listlink in listlinks:
                    order_product = Order_product(
                                    order_id=new_order.id,
                                    product_id=listlink.product.id,
                                    quantity=listlink.quantity
                                    )
                    storage.new(order_product)
            else:
                new_order.products = listlinks
            orders.append(new_order)

        # Save orders to storage
        for order in orders:
            order.save()

        self.send_orders_to_shops(orders)
        self.link_orders_to_user(orders)

        return orders

    def remove_product(self, product_id):
        """ Removes a product from a shop_list """
        from models import storage

        found = False
        if GH_STORAGE_TYPE == "db":
            listlinks = self.products
            for listlink in listlinks:
                if product_id == listlink.product_id:
                    storage.delete(listlink)
                    found = True
        else:
            product_ids = self.products
            if product_id in product_ids:
                product_ids.remove(product_id)
                found = True

        if found:
            self.save()
            self.update_total_cost()
            return True

        return False

    def __init__(self, *args, **kwargs):
        """Initialization of instances"""
        super().__init__(*args, **kwargs)
