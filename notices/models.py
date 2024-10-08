from django.db import models

class Notice(models.Model):
    title     = models.CharField(max_length=100)
    content   = models.CharField(max_length=1000)
    date      = models.DateTimeField()
    important = models.BooleanField()
    expired   = models.BooleanField()

    def __str__(self):
        return self.title