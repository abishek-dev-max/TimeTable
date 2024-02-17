from os import environ

class Config(object):

    SECRET_KEY = environ.get("SECRET_KEY", "52fc4156f99dd3931995d6b99a751581")
