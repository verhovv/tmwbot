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
    model_nickname = fields.TextField()
    max_working = fields.IntField()
    time_mode = fields.TextField()
    start_time = fields.IntField()
    end_time = fields.IntField(default=0)
    working = fields.IntField(default=0)
    started = fields.BooleanField(default=False)
    active = fields.BooleanField(default=True)


class TaskStorage(Model):
    user_id = fields.ForeignKeyField('models.Users')
    task_id = fields.ForeignKeyField('models.Tasks')
    model_nickname = fields.TextField()
    failed = fields.BooleanField(default=False)
    finished = fields.BooleanField(default=False)
