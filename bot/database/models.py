from tortoise.models import Model
from tortoise import fields


class Users(Model):
    id = fields.IntField(pk=True)
    lang = fields.TextField(default='ru')
    model_nickname = fields.TextField(default='')
    chaturbate_nickname = fields.TextField(default='')
    balance = fields.FloatField(default=10000)
    state = fields.TextField(default='choosing language')
