"""
Contains category class implementation
"""

from .base_model import BaseModel


class Category(BaseModel):
    """Blueprint for the category model"""
    name = ""
    description = ""
    image_url = ""

    def __init__(self, *args, **kwargs):
        """Initaialization of instances"""
        super().__init__(*args, **kwargs)
