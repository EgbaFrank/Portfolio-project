"""
Contains blueprint for the user model
"""
from .base_model import BaseModel


class User(BaseModel):
    """Blueprint for the user model"""
    first_name = ""
    last_name = ""
    password = ""
    email = ""
    contact_info = ""
    
    def __init__(self, *args, **kwargs):
        """initialization of user objects"""
        super().__init__(*args, **kwargs)
