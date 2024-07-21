from django.db import models

class Activity(models.Model):
    name     = models.CharField(max_length=100)
    jjang    = models.ForeignKey('members.Member', models.PROTECT, related_name='%(class)s_jjang')
    members  = models.ManyToManyField('members.Member', related_name='%(class)s', blank=True)

    class Meta:
        abstract = True

class Study(Activity):
    pass

class Project(Activity):
    pass
