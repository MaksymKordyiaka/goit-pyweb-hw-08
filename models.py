from mongoengine import Document, StringField, ListField, ReferenceField, BooleanField


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField(required=True)
    born_location = StringField(required=True)
    description = StringField(required=True)


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField(required=True)


class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    email_sent = BooleanField(default=False)