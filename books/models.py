from django.db import models

class Book(models.Model):
    id          = models.CharField(primary_key=True, max_length=100)
    name        = models.CharField(max_length=100)
    author      = models.CharField(max_length=100)
    available   = models.BooleanField()
    tags        = models.ManyToManyField('BookTag', related_name='books', blank=True)
    donor       = models.ForeignKey('members.Member', models.PROTECT, blank=True, null=True)
    image       = models.CharField(max_length=10, blank=True)

    def to_json(self, fields):
        return {field.name: field.value_from_object(self) for field in self._meta.get_fields() if field.name in fields}
    
    def __str__(self):
        return f'{self.name}'

class BookRecord(models.Model):
    borrower        = models.ForeignKey('members.Member', models.PROTECT)
    book            = models.ForeignKey(Book, models.PROTECT)
    start           = models.DateField()
    actual_return   = models.DateField(null=True)
    

class BookTag(models.Model):
    tag = models.CharField(primary_key=True, max_length=100, unique=True)

    def __str__(self):
        return f'#{self.tag}'
    