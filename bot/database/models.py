from tortoise.models import Model
from tortoise import fields


class Users(Model):
    id = fields.IntField(pk=True)
    lang = fields.TextField(default='ru')
    model_nickname = fields.TextField(default='')
    chaturbate_nickname = fields.TextField(default='')
    balance = fields.FloatField(default=10000)
    state = fields.TextField(default='choosing language')


class Tasks(Model):
    max_working = fields.IntField()
    time_mode = fields.TextField()
    start_time = fields.IntField(default=0)
    end_time = fields.IntField(default=0)
    working = fields.IntField(default=0)
    started = fields.BooleanField(default=False)
    active = fields.BooleanField(default=True)
    finished = fields.BooleanField(default=False)
    coins_after_ending = fields.IntField(default=0)

    user = fields.ForeignKeyField('models.Users')


class TaskStorage(Model):
    user = fields.ForeignKeyField('models.Users')
    task = fields.ForeignKeyField('models.Tasks')
    failed = fields.BooleanField(default=False)
    finished = fields.BooleanField(default=False)
    start_time = fields.IntField(default=0)
