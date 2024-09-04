from django.db import models

class ActivityState:
    BEFORE_RECRUIT = 'before_recruit'
    RECRUITING = 'recruiting'
    RUNNING = 'running'
    
    choices = [
        (BEFORE_RECRUIT, '모집 예정'),
        (RECRUITING, '모집 중'),
        (RUNNING, '모집 마감')
    ]

class Event(models.Model):
    name         = models.CharField(max_length=100)
    description  = models.CharField(max_length=1000)
    start_time   = models.DateTimeField()
    end_time     = models.DateTimeField()
    place        = models.CharField(max_length=100) 
    this_week    = models.BooleanField()
    
class ActivityTag(models.Model):
    tag = models.CharField(max_length=100, primary_key=True)

class Study(models.Model):
    name        = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    leader      = models.ForeignKey('members.Member', models.PROTECT, related_name='running_studies')
    members     = models.ManyToManyField('members.Member', related_name='studies')
    tags        = models.ManyToManyField('ActivityTag', related_name='studies', blank=True)
    state       = models.CharField(choices=ActivityState.choices, max_length=14)
    image       = models.BooleanField()
    link        = models.CharField(max_length=200)

class Project(models.Model):
    name        = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    leader      = models.ForeignKey('members.Member', models.PROTECT, related_name='running_projects')
    members     = models.ManyToManyField('members.Member', related_name='projects')
    tags        = models.ManyToManyField('ActivityTag', related_name='projects', blank=True)
    state       = models.CharField(choices=ActivityState.choices, max_length=14)
    image       = models.BooleanField()
    link        = models.CharField(max_length=200)
