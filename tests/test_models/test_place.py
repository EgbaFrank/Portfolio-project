#!/usr/bin/bash python3
"""
Contains test cases for the place class
"""
import unittest
from models.place import Place
from models.base_model import BaseModel


class TestPlace(unittest.TestCase):
    """Test cases for the place class"""
    def setUp(self):
        """Sets up test environment"""
        self.place = Place()

    def test_docs(self):
        """Test the place class for docstrings"""
        self.assertIsNotNone(Place.__module__.__doc__)
        self.assertIsNotNone(Place.__class__.__doc__)
        self.assertIsNotNone(Place.__init__.__doc__)

    def test_attributes(self):
        """Test cases for attributes validity"""
        self.assertIsInstance(self.place, BaseModel)
        self.assertTrue(hasattr(self.place, "name"))
        self.assertEqual(self.place.name, "")
        self.assertTrue(hasattr(self.place, "created_at"))
        self.assertTrue(hasattr(self.place, "updated_at"))
