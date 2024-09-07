#!/usr/bin/env python3
"""
Contains test cases for the category class
"""
import unittest
from models.category import Category
from models.base_model import BaseModel


class TestCategory(unittest.TestCase):
    """Test cases for the category class"""
    def setUp(self):
        """Sets up test environment"""
        self.category = Category()

    def test_docs(self):
        """Test the category class for docstrings"""
        self.assertIsNotNone(Category.__module__.__doc__)
        self.assertIsNotNone(Category.__class__.__doc__)
        self.assertIsNotNone(Category.__init__.__doc__)

    def test_attributes(self):
        """Test cases for attributes validity"""
        self.assertIsInstance(self.category, BaseModel)
        self.assertTrue(hasattr(self.category, "name"))
        self.assertEqual(self.category.name, "")
        self.assertTrue(hasattr(self.category, "description"))
        self.assertEqual(self.category.description, "")
        self.assertTrue(hasattr(self.category, "image_url"))
        self.assertEqual(self.category.image_url, "")
        self.assertTrue(hasattr(self.category, "created_at"))
        self.assertTrue(hasattr(self.category, "updated_at"))
