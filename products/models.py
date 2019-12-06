from django.db import models
from custom_auth.models import CustomUser,Product


class Sprint(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sprints')
    current = models.BooleanField(default=True)
    capacity = models.PositiveSmallIntegerField()
    total_effort = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(max_length=2, choices=[('NS', 'Not Started'), ('P', 'In Progress'), ('D', 'Done')],
                              default='NS')
    end_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Sprint {self.id}"