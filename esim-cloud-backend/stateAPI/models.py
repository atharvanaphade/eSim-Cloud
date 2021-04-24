from django.contrib.auth.models import Group, User
from django.contrib.auth import *
from django.db import models

# Create your models here.

class State(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=256, null=False)
    public = models.BooleanField(default=False)
    info = models.CharField(max_length=256)

    def __str__(self):
        return self.title

class Delta(models.Model):
    title = models.CharField(max_length=256)
    init_state = models.ForeignKey(State, related_name='prev_state', null=True, on_delete=models.SET_NULL)
    new_state = models.ForeignKey(State, related_name='new_state', null=True, on_delete=models.SET_NULL)
    user_type = models.ManyToManyField(Group, related_name='user_type')
    creator = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class DeltaMetadata(models.Model):
    id = models.AutoField(primary_key=True)
    circuit = models.ForeignKey('publishAPI.Circuit', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

class Groups(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    states = models.ManyToManyField(State, related_name='groups')
    is_arduino = models.BooleanField(default=False)

    def __str__(self):
        return str(self.group.name)
