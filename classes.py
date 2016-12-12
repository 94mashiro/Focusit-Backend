from mongoengine import *

class Article(Document):
    title = StringField()
    author = StringField()
    url = StringField()
    tag = ListField()
    origin = StringField()
    createdAt = DateTimeField()
