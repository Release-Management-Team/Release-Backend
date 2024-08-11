from django.db import models

class Book(models.Model):
    id          = models.CharField(primary_key=True, max_length=100)
    name        = models.CharField(max_length=100)
    author      = models.CharField(max_length=100)
    available   = models.BooleanField()
    tags        = models.ManyToManyField('BookTag', related_name='books', blank=True)
    donor       = models.ForeignKey('members.Member', models.PROTECT, blank=True, null=True)
    image       = models.CharField(max_length=10, blank=True)
        
    def __str__(self):
        return f'{self.name}'

class BookRecord(models.Model):
    borrower = models.ForeignKey('members.Member', models.PROTECT) # student id (foreign key)
    book = models.ForeignKey(Book, models.PROTECT)
    start_date = models.DateField()
    actual_return = models.DateField(null=True)

class BookTag(models.Model):
    tag = models.CharField(primary_key=True, max_length=100, unique=True)

    def __str__(self):
        return self.tag