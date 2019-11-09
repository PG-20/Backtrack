from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=30, blank=False)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    created_at = models.DateField()

    def __str__(self):
        return self.name

class Sprint(models.Model):
    current = models.BooleanField(default=True)
    capacity = models.PositiveSmallIntegerField()
    total_effort = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(max_length=2, choices=[('NS', 'Not Started'), ('P', 'In Progress'), ('D', 'Done')],
                              default='NS')
    end_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Sprint {self.id}"