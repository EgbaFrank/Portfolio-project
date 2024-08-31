"""
Defines the attributes of the BaseModel class
"""
import uuid
from models import storage
from datetime import datetime


class BaseModel:
    """Blueprint for BaseModel instances"""

    def __init__(self, *args, **kwargs):
        """Instantiates a new BaseModel object"""
        # Check if instance is new
        has_id = kwargs.get('id')

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

        if not has_id:
            storage.new(self)

    def __str__(self):
        """Returns a formatted string representation of the instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Saves the instance to available storage"""
        self.updated_at = datetime.utcnow()
        storage.save()

    def to_dict(self):
        """Returns a dictionary representation of the instance"""
        obj_dict = {
            key: (value.isoformat() if isinstance(value, datetime) else value)
            for key, value in self.__dict__.items()
        }
        obj_dict['__class__'] = self.__class__.__name__

        return obj_dict

    def delete(self):
        """delete the current instance from storage"""
        storage.delete(self)
