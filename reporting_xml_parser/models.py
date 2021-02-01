from django.db import models
from django.contrib.auth.models import User
from ..mlpool.models import *


class Request(models.Model):
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
    chosen_model = models.ForeignKey(Model, on_delete=models.DO_NOTHING)
    user_data = models.FileField()
    date_added = models.DateTimeField(auto_now_add=True)

    NEW, DONE, ERROR = 'new', 'done', 'error'
    STATUS_CHOICES = [
        (NEW, 'In progress'),
        (DONE, 'Successfully finished'),
        (ERROR, 'Ended up with error'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NEW)

    WRONG_INPUT, SERVER_ERROR, TIMEOUT, NONE = 'INPUT', 'SERVER', 'TIMEOUT', 'NONE'
    ERROR_DESCRIPTION_CHOICES = [
        (WRONG_INPUT, 'Введенные данные содержат ошибку'),
        (SERVER_ERROR, 'Ошибка сервера. Попробуйте позже.'),
        (TIMEOUT, 'Слишком долго'),
        (NONE, 'Ошибок нет')
    ]
    error_description = models.CharField(max_length=100, choices=STATUS_CHOICES, default=NONE)

    model_spent_time = models.TimeField(default=0)

    def __str__(self):
        return 'Request ' + str(self.id)


class Result(models.Model):
    model = models.ForeignKey(Model, on_delete=models.DO_NOTHING)
    request = models.ForeignKey(Request, on_delete=models.DO_NOTHING)
    date_added = models.DateTimeField(auto_now_add=True)
    prediction = models.BinaryField()

    def __str__(self):
        return 'result' + str(self.id) + ' from ' + str(self.model.model_name)


class Response(models.Model):
    result = models.ForeignKey(Result, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_added = models.DateTimeField(auto_now_add=True)
    expert_answers = models.BinaryField()
