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

    def to_dict(self, fields):
        data = {}
        for name in fields:
            if name == 'leader':
                data[name] = self.leader.id
            elif name == 'members':
                data[name] = [member.id for member in self.members.all()]
            elif name == 'tags':
                data[name] = [tag.tag for tag in self.tags.all()]
            else:
                data[name] = self._meta.get_field(name).value_from_object(self)

        return data


class Project(models.Model):
    name = models.CharField(max_length=100)
    leader = models.ForeignKey('members.Member', models.PROTECT, related_name='running_projects')
    members = models.ManyToManyField('members.Member', related_name='projects')
    description = models.CharField(max_length=1000)

    def to_dict(self, fields):
        data = {}
        for name in fields:
            if name == 'leader':
                data[name] = self.leader.id
            elif name == 'members':
                data[name] = [member.id for member in self.members.all()]
            else:
                data[name] = self._meta.get_field(name).value_from_object(self)

        return data
    