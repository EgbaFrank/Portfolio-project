#!/usr/bin/bash python3
"""
Contains test cases for the user class
"""
import unittest
from models.user import User
from models.base_model import BaseModel


class TestUser(unittest.TestCase):
    """Test cases for the user class"""
    def setUp(self):
        """Sets up test environment"""
        self.user = User()

    def test_docs(self):
        """Test the user class for docstrings"""
        self.assertIsNotNone(User.__module__.__doc__)
        self.assertIsNotNone(User.__class__.__doc__)
        self.assertIsNotNone(User.__init__.__doc__)

    def test_attributes(self):
        """Test cases for attributes validity"""
        self.assertIsInstance(self.user, BaseModel)
        self.assertTrue(hasattr(self.user, "first_name"))
        self.assertEqual(self.user.first_name, "")
        self.assertTrue(hasattr(self.user, "last_name"))
        self.assertEqual(self.user.last_name, "")
        self.assertTrue(hasattr(self.user, "email"))
        self.assertEqual(self.user.email, "")
        self.assertTrue(hasattr(self.user, "password"))
        self.assertEqual(self.user.password, "")
        self.assertTrue(hasattr(self.user, "contact_info"))
        self.assertEqual(self.user.contact_info, "")
        self.assertTrue(hasattr(self.user, "created_at"))
        self.assertTrue(hasattr(self.user, "updated_at"))
