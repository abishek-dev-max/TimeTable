import os

class Config(object):

    SECRET_KEY = os.environ.get("SECRET_KEY", "52fc4156f99dd3931995d6b99a751581")
