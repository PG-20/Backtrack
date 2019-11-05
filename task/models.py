from django.db import models
from products.models import User
from productBacklog.models import ProductBacklog
# Create your models here.

class Task(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    effort=models.IntegerField(default=0)
    status=models.CharField(max_length=2,choices=[('TD','To-Do'),('P','In Progress'),('D','Done')],default='TD')
    pbi=models.ForeignKey(ProductBacklog,on_delete=models.CASCADE)
    description=models.CharField(max_length=1000)

class Sprint(models.Model):
    sprint_no=models.PositiveSmallIntegerField()
    current=models.BooleanField(default=True) 
    capacity=models.PositiveSmallIntegerField()
    total_effort=models.PositiveSmallIntegerField(default=0)