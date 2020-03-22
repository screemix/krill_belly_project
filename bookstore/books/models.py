from django.db import models
from datetime import datetime

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    date_of_release = models.DateTimeField(default = datetime.now, blank=True)
    description = models.TextField(blank=True)
    genre = models.CharField(max_length=200, default = 'Роман')
    cost = models.IntegerField(default=500)
    def __str__(self):
        return self.title
