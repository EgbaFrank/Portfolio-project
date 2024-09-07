#!/usr/bin/env python3
"""
Contains test cases for the shop class
"""
import unittest
from models.shop import Shop
from models.base_model import BaseModel


class TestShop(unittest.TestCase):
    """Test cases for the shop class"""

    def setUp(self):
        """Sets up test environment"""
        self.shop = Shop()

    def test_docs(self):
        """Test the shop class for docstrings"""
        self.assertIsNotNone(Shop.__module__.__doc__)
        self.assertIsNotNone(Shop.__class__.__doc__)
        self.assertIsNotNone(Shop.__init__.__doc__)

    def test_attributes(self):
        """Test cases for attributes validity"""
        self.assertIsInstance(self.shop, BaseModel)
        self.assertTrue(hasattr(self.shop, "name"))
        self.assertEqual(self.shop.name, "")
        self.assertTrue(hasattr(self.shop, "api_url"))
        self.assertEqual(self.shop.api_url, "")
        self.assertTrue(hasattr(self.shop, "address"))
        self.assertEqual(self.shop.address, "")
        self.assertTrue(hasattr(self.shop, "place_id"))
        self.assertEqual(self.shop.place_id, "")
        self.assertTrue(hasattr(self.shop, "created_at"))
        self.assertTrue(hasattr(self.shop, "updated_at"))
