"""
Defines the attributes of the BaseModel class
"""
import uuid
from models import storage, storage_type
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    """Blueprint for BaseModel instances"""
    if storage_type == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, nullable=False)
        updated_at = Column(DateTime, nullable=False)

    def __init__(self, *args, **kwargs):
        """Instantiates a new BaseModel object"""
        self.id = kwargs.pop('id', str(uuid.uuid4()))
        try:
            self.created_at = datetime.strptime(
                                kwargs.pop('created_at'),
                                '%Y-%m-%dT%H:%M:%S.%f')
        except (KeyError, ValueError):
            self.created_at = datetime.utcnow()
        try:
            self.updated_at = datetime.strptime(
                                kwargs.pop('updated_at'),
                                '%Y-%m-%dT%H:%M:%S.%f')
        except (KeyError, ValueError):
            self.updated_at = datetime.utcnow()

        kwargs.pop('__class__', None)

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        """Returns a formatted string representation of the instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Saves the instance to available storage"""
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Returns a dictionary representation of the instance"""
        obj_dict = {
            key: (value.isoformat() if isinstance(value, datetime) else value)
            for key, value in self.__dict__.items()
        }
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict.pop("_sa_instance_state", None)

        return obj_dict

    def delete(self):
        """delete the current instance from storage"""
        storage.delete(self)
