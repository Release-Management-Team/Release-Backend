from django.db import models

class ActivityState(models.IntegerChoices):
    BEFORE_RECRUIT  = 0, 'before_recruit'
    RECRUITING      = 1, 'recruiting'
    RUNNING         = 2, 'running'


class ActivityInfo(models.IntegerChoices):
    PROJECT = 0, '프로젝트'
    STUDY   = 1, '스터디'


class Activity(models.Model):
    title       = models.CharField(max_length=100)
    content     = models.CharField(max_length=1000)
    leader      = models.ForeignKey('members.Member', models.PROTECT, related_name='running_studies')
    members     = models.ManyToManyField('members.Member', related_name='studies')
    image       = models.BooleanField(default=False)
    state       = models.IntegerField(choices=ActivityState)
    info        = models.IntegerField(choices=ActivityInfo)
    link        = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Event(models.Model):
    title        = models.CharField(max_length=100)
    content  = models.CharField(max_length=1000)
    start_time   = models.DateTimeField()
    place        = models.CharField(max_length=100) 

    def __str__(self):
        return self.title