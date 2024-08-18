from flask import json

class JSONLoader:
    @classmethod
    def load(cls, path):
        return json.load(open(path))