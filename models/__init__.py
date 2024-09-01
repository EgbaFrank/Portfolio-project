from os import getenv

if getenv("GH_TYPE_STORAGE") == "db":
    storage_type = "db"
    pass

else:
    from .engine.file_storage import FileStorage
    storage = FileStorage()
    storage_type = "file"

storage.reload()
