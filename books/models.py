from django.db import models

class Book(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    available = models.BooleanField()
    tags = models.ManyToManyField("BookTag")

class BookRecord(models.Model):
    borrower = models.IntegerField() # student id (foreign key)
    book = models.ForeignKey(Book, models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    actual_return = models.DateField(null=True)

class BookTag(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return self.tag