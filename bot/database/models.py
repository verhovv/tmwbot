from tortoise.models import Model
from tortoise import fields


class Users(Model):
    id = fields.IntField(pk=True)
    lang = fields.TextField(default='ru')
    model_name = fields.TextField(default='')
    state = fields.TextField(default='choosing language')
