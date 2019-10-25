from django.db import models
from products.models import User
from datetime import datetime
from django.urls import reverse
# Create your models here.

class ProductBacklog(models.Model):
    title=models.CharField(max_length=100)
    effort=models.DecimalField(max_digits=100,decimal_places=3)
    story_points=models.DecimalField(max_digits=100,decimal_places=3)
    effort_done=models.DecimalField(max_digits=100,decimal_places=3)
    status=models.CharField(max_length=2,choices=[('TD','To-Do'),('P','In Progress'),('D','Done')],default='TD')
    last_updated=models.DateTimeField(auto_now=False,auto_now_add=False,default=datetime.now())
    pbi_type=models.CharField(max_length=2,choices=[('B','Bug'),('E','Epic'),('US','User Story')],default='US')
    sprint_no=models.PositiveSmallIntegerField()
    main_dev=models.ForeignKey(User,on_delete=models.CASCADE,related_name="main_project_pbis")
    other_dev=models.ManyToManyField(User)
    priority=models.DecimalField(max_digits=100,decimal_places=3)

    def get_absolute_url(self):

        # from django.core.urlresolvers import reverse
        # return reverse('', kwargs={'pk': self.pk})
        return f"/products/{self.id}/"