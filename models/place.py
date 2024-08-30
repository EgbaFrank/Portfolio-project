"""
Contains place class implementation
"""
from .base_model import BaseModel


class Place(BaseModel):
    """Blueprint for the place model"""
    name = ""

    def __init__(self, *args, **kwargs):
        """Initiaalization of instances"""
        super().__init__(*args, **kwargs)
