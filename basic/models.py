from django.db import models
from django.contrib.auth.models import User

class Iphones(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    name=models.CharField(max_length=100,null=True)
    site=models.CharField(max_length=10000000000,null=True)
   


class Samsungs(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    name=models.CharField(max_length=100,null=True)
    price=models.IntegerField(null=True)
    desc=models.TextField(null=True)



    