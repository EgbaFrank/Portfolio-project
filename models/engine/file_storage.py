"""
Contains the file storage functionality
"""
import json

class FileStorage():
    """Blueprint for FileStorage objects"""
    __file_path = "data.json"
    __objects = {}

    def all(self, cls=None):
        """Returns all stored objects"""
        if cls:
            cls_objs = {key: val for key, val in self.__objects.items() if cls == val.__class__ or cls == val.__class__.__name__}
            return cls_objs

        return self.__objects

    def new(self, obj):
        """Adds a new object for storage"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Stores objects as json"""
        stor_dict = {key: value.to_dict() for key, value in self.__objects.items()}

        with open(self.__file_path, 'w') as file:
            json.dump(stor_dict, file)

    def reload(self):
        """Retrieve stored objects"""
        from models.base_model import BaseModel
        from models.user import User
        from models.shop import Shop
        from models.product import Product
        from models.order import Order
        from models.category import Category
        from models.place import Place
        from models.shop_list import Shop_list
        cls_lst = {
                "BaseModel": BaseModel,
                "User": User,
                "Shop": Shop,
                "Product": Product,
                "Order": Order,
                "Category": Category,
                "Place": Place,
                "Shop_list": Shop_list
                }

        try:
            with open(self.__file_path) as file:
                data = json.load(file)
                for objs_dict in data.values():
                    cls = cls_lst[objs_dict["__class__"]]
                    self.new(cls(**objs_dict))
        except FileNotFoundError:
            pass

    def reset(self):
        """Resets the FileStorage __object"""
        self.__objects = {}

    def get(self, cls, id):
        """Retrieves a specific object"""
        key = cls.__name__ + '.' + id
        return self.all(cls).get(key)

    def count(self, cls=None):
        """Retrieves the number of all or specific instances"""
        return len(self.all(cls))
