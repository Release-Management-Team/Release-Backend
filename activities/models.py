from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

class StudyTag(models.Model):
    tag = models.CharField(max_length=100)

class Study(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    leader = models.ForeignKey('members.Member', models.PROTECT, related_name='running_studies')
    members = models.ManyToManyField('members.Member', related_name='studies')
    tags = models.ManyToManyField('StudyTag', related_name='studies', blank=True)

class Project(models.Model):
    name = models.CharField(max_length=100)
    leader = models.ForeignKey('members.Member', models.PROTECT, related_name='running_projects')
    members = models.ManyToManyField('members.Member', related_name='projects')
    description = models.CharField(max_length=1000)

