#!/usr/bin/env python3
"""
Contains test cases for the product class
"""
import unittest
from models.product import Product
from models.base_model import BaseModel


class TestProduct(unittest.TestCase):
    """Test cases for the product class"""
    def setUp(self):
        """Sets up test environment"""
        self.product = Product()

    def test_docs(self):
        """Test the product class for docstrings"""
        self.assertIsNotNone(Product.__module__.__doc__)
        self.assertIsNotNone(Product.__class__.__doc__)
        self.assertIsNotNone(Product.__init__.__doc__)

    def test_attributes(self):
        """Test cases for attributes validity"""
        self.assertIsInstance(self.product, BaseModel)
        self.assertTrue(hasattr(self.product, "name"))
        self.assertEqual(self.product.name, "")
        self.assertTrue(hasattr(self.product, "price"))
        self.assertEqual(self.product.price, 0)
        self.assertTrue(hasattr(self.product, "brand"))
        self.assertEqual(self.product.brand, "")
        self.assertTrue(hasattr(self.product, "image"))
        self.assertEqual(self.product.image, "")
        self.assertTrue(hasattr(self.product, "unit"))
        self.assertEqual(self.product.unit, "")
        self.assertTrue(hasattr(self.product, "shop_ids"))
        self.assertEqual(self.product.shop_ids, [])
        self.assertTrue(hasattr(self.product, "category_id"))
        self.assertEqual(self.product.category_id, "")
        self.assertTrue(hasattr(self.product, "created_at"))
        self.assertTrue(hasattr(self.product, "updated_at"))
