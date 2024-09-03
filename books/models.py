from django.db import models
from django.utils import timezone

class BookState:
    AVAILABLE   = 'available'
    RENTED      = 'rented'
    UNAVAILABLE = 'unavailable'
    choices = [
        (AVAILABLE,   '대여 가능'),
        (RENTED,      '대여 중'),
        (UNAVAILABLE, '대여 불가')
    ]

class Book(models.Model):
    id           = models.CharField(primary_key=True, max_length=100)
    title        = models.CharField(max_length=100)
    author       = models.CharField(max_length=100)
    availability = models.CharField(max_length=11, choices=BookState.choices)
    tags         = models.ManyToManyField('BookTag', related_name='books', blank=True)
    image        = models.BooleanField()
        
    def __str__(self):
        return f'{self.title}'

class BookRecord(models.Model):
    borrower = models.ForeignKey('members.Member', models.PROTECT) # student id (foreign key)
    book = models.ForeignKey(Book, models.PROTECT)
    start_date = models.DateField(default=timezone.now)
    actual_return = models.DateField(null=True)

class BookTag(models.Model):
    tag = models.CharField(primary_key=True, max_length=100, unique=True)

    def __str__(self):
        return self.tag