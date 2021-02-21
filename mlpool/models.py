from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date, time


class Project(models.Model):
    project_name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_name


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    task_name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name


class MLModel(models.Model):
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
    model_name = models.CharField(max_length=200)
    version = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    date_added = models.DateTimeField(auto_now_add=True)
    binary_body = models.FileField(upload_to='uploads')
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.model_name


class UserRequest(models.Model):
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
    ml_model = models.ForeignKey(MLModel, on_delete=models.DO_NOTHING)
    date_added = models.DateTimeField(auto_now_add=True)
    spent_time = models.IntegerField(default=0)

    STATUS_CHOICES = (
        ('OK', 'OK'),
        ('ERROR', 'ERROR')
    )
    status = models.CharField(default='OK', choices=STATUS_CHOICES, max_length=40)

    def __str__(self):
        return "request #" + str(self.id)


class Result(models.Model):
    ml_model = models.ForeignKey(MLModel, on_delete=models.DO_NOTHING)
    user_request = models.ForeignKey(UserRequest, on_delete=models.DO_NOTHING)
    date_added = models.DateTimeField(auto_now_add=True)
    input_data = models.CharField(max_length=4000)
    prediction = models.CharField(max_length=4000)

    def __str__(self):
        return "result #" + str(self.id)


class Response(models.Model):
    result = models.ForeignKey(Result, on_delete=models.DO_NOTHING)
    date_added = models.DateTimeField(auto_now_add=True)
    expert_target = models.CharField(max_length=4000)

    def __str__(self):
        return "response #" + str(self.id)
