#!/usr/bin/env python3
"""
Test cases for BaseModel class
"""
import unittest
from datetime import datetime
from unittest.mock import patch
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """Test BaseModel attributes and documentations"""
    @patch('models.engine.file_storage.FileStorage.new')
    def setUp(self, mock_new):
        """Sets up test environment"""
        self.base_model = BaseModel()

    def test_docs(self):
        """Test BaseModel for docstrings"""
        self.assertIsNotNone(BaseModel.__module__.__doc__)
        self.assertIsNotNone(BaseModel.__class__.__doc__)
        self.assertIsNotNone(BaseModel.__init__.__doc__)
        self.assertIsNotNone(BaseModel.__str__.__doc__)
        self.assertIsNotNone(BaseModel.save.__doc__)
        self.assertIsNotNone(BaseModel.to_dict.__doc__)

    def test_creation(self):
        """Test for proper BaseModel creation"""
        self.assertIsInstance(self.base_model, BaseModel)
        self.assertIsNotNone(self.base_model.id)
        self.assertIsInstance(self.base_model.id, str)
        self.assertIsInstance(self.base_model.created_at, datetime)
        self.assertIsInstance(self.base_model.updated_at, datetime)

        # Test case for empty kwargs creation
        base_model = BaseModel(**{})

        self.assertIsInstance(base_model, BaseModel)
        self.assertIsNotNone(base_model.id)
        self.assertIsInstance(base_model.id, str)
        self.assertIsInstance(base_model.created_at, datetime)
        self.assertIsInstance(base_model.updated_at, datetime)

        # Test for unique ids
        self.assertNotEqual(base_model.id, self.base_model.id)

    @patch('models.engine.file_storage.FileStorage.save')
    def test_save(self, mock_save):
        """Test cases for the save method"""
        old_timestamp = self.base_model.updated_at
        self.base_model.save()
        self.assertNotEqual(self.base_model.updated_at, old_timestamp)
        self.assertGreater(self.base_model.updated_at, old_timestamp)

        mock_save.assert_called_once_with()

    def test_str_format(self):
        """Test for proper print format"""
        expected_print = (
            f"[BaseModel] ({self.base_model.id}) {self.base_model.__dict__}"
        )
        self.assertEqual(expected_print, str(self.base_model))

    def test_to_dict_method(self):
        """Test for correct BaseModel dictionary representation"""
        model_dict = self.base_model.to_dict()
        self.assertEqual(model_dict.get('id'), self.base_model.id)
        self.assertEqual(
                model_dict.get('created_at'),
                self.base_model.created_at.isoformat()
        )
        self.assertEqual(
                model_dict.get('updated_at'),
                self.base_model.updated_at.isoformat()
        )
        self.assertEqual(model_dict.get('__class__'), 'BaseModel')

    def test_model_re_creation(self):
        """Test instance recreation from dictionary representation"""
        model_dict = self.base_model.to_dict()
        base_model_2 = BaseModel(**model_dict)

        self.assertIsInstance(base_model_2, BaseModel)
        self.assertEqual(self.base_model.id, base_model_2.id)
        self.assertIsInstance(base_model_2.id, str)
        self.assertNotIn('__class__', base_model_2.__dict__)
        self.assertIsInstance(base_model_2.created_at, datetime)
        self.assertEqual(base_model_2.created_at, self.base_model.created_at)
        self.assertIsInstance(base_model_2.updated_at, datetime)
        self.assertEqual(base_model_2.updated_at, self.base_model.updated_at)
