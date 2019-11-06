from django.db import models
from products.models import User
from productBacklog.models import ProductBacklogItem
# Create your models here.

class Task(models.Model):
    owner=models.ForeignKey(User, on_delete=models.CASCADE)
    effort=models.IntegerField(default=0)
    status=models.CharField(max_length=2, choices=[('TD','To-Do'),('P','In Progress'),('D','Done')],default='TD')
    pbi=models.ForeignKey(ProductBacklogItem, on_delete=models.CASCADE)
    description=models.TextField(max_length=1000)

    def __str__(self):
        return self.description
