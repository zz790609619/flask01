
from werkzeug.wrappers import BaseResponse


class User(BaseResponse):
    def __init__(self, name, age):
        super().__init__()
        self.name = name
        self.age = age

