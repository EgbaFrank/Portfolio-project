"""
This module contains the database engine implementation
"""
from os import getenv
from dotenv import load_dotenv
from models.base_model import Base
from models.user import User
from models.shop import Shop
from models.product import Product
from models.order import Order
from models.category import Category
from models.place import Place
from models.shop_list import Shop_list
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

load_dotenv("db_storage.env")


class DBStorage():
    """Blueprint for database storage"""
    __engine = None
    __session = None

    def __init__(self):
        """Insantiate a new db storage object"""
        self.__engine = create_engine(
                'mysql+mysqldb://{}:{}@{}/{}'
                .format(
                    getenv('GrocHub_MYSQL_USER'),
                    getenv('GrocHub_MYSQL_PWD'),
                    getenv('GrocHub_MYSQL_HOST', 'localhost'),
                    getenv('GrocHub_MYSQL_DB')
                ),
                pool_pre_ping=True
        )

        if getenv('GrocHub_ENV') == 'test':
            # Drop tables only in the test environment
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Retrieves specified or all class instances"""
        _objects = {}

        if cls:
            if issubclass(cls, Base):
                objs = self.__session.query(cls).all()

        else:
            objs = []
            classes = [Place, User, Shop, Category, Product, Shop_list, Order]

            for cls in classes:
                objs.extend(
                    self.__session.query(cls).all()
                )
        for obj in objs:
            key = f'{obj.__class__.__name__}.{obj.id}'
            _objects[key] = obj

        return _objects

    def new(self, obj):
        """Add an object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database"""
        Base.metadata.create_all(self.__engine)

        # Create the current database session
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(sess_factory)

    def reset(self):
        """Resets database session"""
        session.rollback()  # Rollback pending changes

    def close(self):
        """Close the current session"""
        self.__session.remove()

    def get(self, cls, id):
        """Retrieves an object"""
        if issubclass(cls, Base):
            return self.__session.query(cls).filter_by(id=id).first()

    def count(self, cls=None):
        """count the number of objects in storage"""
        return len(self.all(cls))
