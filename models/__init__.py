from os import getenv

if getenv("GH_STORAGE_TYPE") == "db":
    from .engine.db_storage import DBStorage
    storage = DBStorage()

else:
    from .engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
