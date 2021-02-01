from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    project_name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    date_added = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('valid', 'Готов к использованию'),
        ('error', 'Отправлен на доработку'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='valid')

    def __str__(self):
        return self.project_name


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    task_name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name


class Model(models.Model):
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
    model_name = models.CharField(max_length=200)
    version = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    date_added = models.DateTimeField(auto_now_add=True)
    # TODO: editable=False => binary_body can not be set by a ModelForm
    binary_body = models.BinaryField()

    def __str__(self):
        return self.model_name


