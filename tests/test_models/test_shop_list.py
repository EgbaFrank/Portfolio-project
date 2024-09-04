#!/usr/bin/bash python3
"""
Contains test cases for the shop_list class
"""
import unittest
from models.shop_list import Shop_list
from models.base_model import BaseModel


class TestShop_list(unittest.TestCase):
    """Test cases for the shop_list class"""
    def setUp(self):
        """Sets up test environment"""
        self.shop_list = Shop_list()

    def test_docs(self):
        """Test the shop_list class for docstrings"""
        self.assertIsNotNone(Shop_list.__module__.__doc__)
        self.assertIsNotNone(Shop_list.__class__.__doc__)
        self.assertIsNotNone(Shop_list.__init__.__doc__)

    def test_attributes(self):
        """Test cases for attributes validity"""
        self.assertIsInstance(self.shop_list, BaseModel)
        self.assertTrue(hasattr(self.shop_list, "user_id"))
        self.assertEqual(self.shop_list.user_id, "")
        self.assertTrue(hasattr(self.shop_list, "total_cost"))
        self.assertEqual(self.shop_list.total_cost, 0)
        self.assertTrue(hasattr(self.shop_list, "product_ids"))
        self.assertEqual(self.shop_list.product_ids, {})
        self.assertTrue(hasattr(self.shop_list, "created_at"))
        self.assertTrue(hasattr(self.shop_list, "updated_at"))
