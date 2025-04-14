from mongoengine import Document, ReferenceField, ListField, StringField, CASCADE, BooleanField


class Contact(Document):
    fullname = StringField(max_length=100, required=True, unique=True)
    email = StringField(max_length=50)
    issend = BooleanField(default=False)
    phone = StringField(max_length=20)
    address = StringField(max_length=200)




