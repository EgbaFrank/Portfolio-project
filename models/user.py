"""
Contains blueprint for the user model
"""
from os import getenv
from .base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Blueprint for the user model"""
    if getenv("GH_STORAGE_TYPE") == "db":
        __tablename__ = "users"

        first_name = Column(String(128))
        last_name = Column(String(128))
        password = Column(String(128), nullable=False)
        email = Column(String(128), nullable=False)
        contact_info = Column(String(60))
        shop_lists = relationship(
                'Shop_list',
                backref='user',
                cascade='all, delete-orphan'
        )

        orders = relationship(
                'Order',
                backref='user',
                cascade='all, delete-orphan'
        )

    else:
        first_name = ""
        last_name = ""
        password = ""
        email = ""
        contact_info = ""
        order_ids = []
        shop_list_ids = []

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
        def shop_lists(self):
            """getter attribute returns the list of Shop_list instances"""
            from .shop_list import Shop_list
            from models import storage
            shop_lists = storage.all("Shop_list")
            return [shop_list for shop_list in shop_lists.values()
                    if shop_list.id in self.shop_list_ids]

        @shop_lists.setter
        def shop_lists(self, value):
            """setter attribute manages shop_lists I/O operations"""
            from .shop_list import Shop_list
            self.shop_list_ids = []
            if isinstance(value, Shop_list):
                if value.id not in self.shop_list_ids:
                    self.shop_list_ids.append(value.id)
            elif isinstance(value, list):
                self.shop_list_ids.extend([
                    shop_list.id for shop_list in value
                    if isinstance(shop_list, Shop_list)
                ])

    def make_shop_list(self):
        """Creates a user shop_list instance"""
        from models.shop_list import Shop_list
        shop_list = Shop_list(user_id=self.id)
        if getenv("GH_STORAGE_TYPE") == "db":
            self.shop_lists.append(shop_list)
        else:
            self.shop_lists = shop_list
        shop_list.save()
        self.save()
        return shop_list

    def __init__(self, *args, **kwargs):
        """initialization of user objects"""
        super().__init__(*args, **kwargs)
