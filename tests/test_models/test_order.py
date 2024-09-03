#!/usr/bin/bash python3
"""
Contains test cases for the order class
"""
import unittest
from models.order import Order
from models.base_model import BaseModel


class TestOrder(unittest.TestCase):
    """Test cases for the order class"""
    def setUp(self):
        """Sets up test environment"""
        self.order = Order()

    def test_docs(self):
        """Test the order class for docstrings"""
        self.assertIsNotNone(Order.__module__.__doc__)
        self.assertIsNotNone(Order.__class__.__doc__)
        self.assertIsNotNone(Order.__init__.__doc__)

    def test_attributes(self):
        """Test cases for attributes validity"""
        self.assertIsInstance(self.order, BaseModel)
        self.assertTrue(hasattr(self.order, "product_ids"))
        self.assertEqual(self.order.product_ids, [])
        self.assertTrue(hasattr(self.order, "status"))
        self.assertEqual(self.order.status, "")
        self.assertTrue(hasattr(self.order, "total_cost"))
        self.assertEqual(self.order.total_cost, 0)
        self.assertTrue(hasattr(self.order, "shop_id"))
        self.assertEqual(self.order.shop_id, "")
        self.assertTrue(hasattr(self.order, "list_id"))
        self.assertEqual(self.order.list_id, "")
        self.assertTrue(hasattr(self.order, "created_at"))
        self.assertTrue(hasattr(self.order, "updated_at"))
