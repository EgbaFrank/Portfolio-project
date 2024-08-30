#!/usr/bin/bash python3
"""
Contains tests for the file storage
"""
import unittest
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from unittest.mock import patch, mock_open, call

class TestFileStorage(unittest.TestCase):
    """Test case for the FileStorage class"""

    @patch('models.storage.new')
    def setUp(self, mock_new):
        """Sets up each test case environment"""
        self.storage = FileStorage()
        self.test = BaseModel()
        self.storage.reset()
        self.data = {f"{self.test.__class__.__name__}.{self.test.id}": self.test.to_dict()}

    def tearDown(self):
        """Cleans up test environment"""
        self.storage.reset()

    def test_docs(self):
        """Test FileStorage for docstrings"""
        self.assertIsNotNone(FileStorage.__module__.__doc__)
        self.assertIsNotNone(FileStorage.__class__.__doc__)
        self.assertIsNotNone(FileStorage.__init__.__doc__)
        self.assertIsNotNone(FileStorage.all.__doc__)
        self.assertIsNotNone(FileStorage.new.__doc__)
        self.assertIsNotNone(FileStorage.save.__doc__)
        self.assertIsNotNone(FileStorage.reload.__doc__)

    def test_all(self):
        """Test cases for the all method"""
        objs = self.storage.all()
        self.assertEqual(objs, {})
        self.assertIsInstance(objs, dict)

    @patch('models.storage.new')
    def test_new(self, mock_new):
        """Test cases for the new method"""
        test = BaseModel()
        self.storage.new(test)
        key = f"{test.__class__.__name__}.{test.id}"
        self.assertIn(key, self.storage.all())
        self.assertEqual(len(self.storage.all()), 1)

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save(self, mock_json_dump, mock_file):
        """Test cases for the save method"""
        self.storage.new(self.test)
        self.storage.save() 
        mock_file.assert_called_once_with("data.json", 'w')
        mock_json_dump.assert_called_once_with(self.data, mock_file())

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    @patch("json.dump")
    def test_reload(self, mock_json_dump, mock_json_load, mock_file):
        """Test cases for the reload method"""
        # mock data for json.dump during save
        mock_json_dump.return_value = None

        # Simulate saving to file
        self.storage.save()
        self.storage.reset()

        # Check that storage is empty after reset
        self.assertEqual(self.storage.all(), {})

        # Mock the data returned by json.load during reload
        mock_json_load.return_value = self.data

        # Reload storage with mocked data
        self.storage.reload()

        key = f"{self.test.__class__.__name__}.{self.test.id}"

        # Assert storage now contains reloaded data
        self.assertIn(key, self.storage.all())

        # Assert open() was called exactly twice, once for reading and once for writing
        mock_file.assert_has_calls([
                            call("data.json"),
                            call("data.json", 'w')
                            ], any_order=True)

        # Assert json.load was called exactly once
        mock_json_load.assert_called_once_with(mock_file())
