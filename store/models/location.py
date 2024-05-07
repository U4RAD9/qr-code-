from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100, default=None)

    def __str__(self):
        return self.name