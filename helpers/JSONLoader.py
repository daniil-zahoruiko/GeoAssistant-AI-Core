from flask import json

class JSONLoader:
    data = None

    @classmethod
    def load(cls, path):
        if cls.data is None:
            cls.data = json.load(open(path))
        return cls.data