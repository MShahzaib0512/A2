from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Bank(models.Model):
 bank_id = models.AutoField(primary_key=True)
 name = models.CharField(max_length=100)
 description = models.CharField(max_length=100)
 inst_num = models.CharField(max_length=100)
 swift_code = models.CharField(max_length=100)
 admin = models.ForeignKey(User, on_delete=models.CASCADE)
 
class Branch(models.Model):
   branch_id = models.AutoField(primary_key=True)  
   name = models.CharField(max_length=100)
   transit_num = models.CharField(max_length=100)
   address = models.CharField(max_length=100)
   email = models.EmailField(max_length=100) 
   capacity = models.PositiveIntegerField()  
   bank = models.ForeignKey(Bank, on_delete=models.CASCADE,related_name='branches')