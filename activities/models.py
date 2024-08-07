from django.db import models

class Study(models.Model):
    name = models.CharField(max_length=100)
    president = models.ForeignKey('members.Member', models.PROTECT, related_name='running_studies')
    members = models.ManyToManyField('members.Member', related_name='studies')
    goal = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)

    def to_dict(self, fields):
        data = {}
        for name in fields:
            if name == 'president':
                data[name] = self.president.id
            elif name == 'members':
                data[name] = [member.id for member in self.members.all()]
            else:
                data[name] = self._meta.get_field(name).value_from_object(self)

        return data


class Project(models.Model):
    name = models.CharField(max_length=100)
    president = models.ForeignKey('members.Member', models.PROTECT, related_name='running_projects')
    members = models.ManyToManyField('members.Member', related_name='projects')
    description = models.CharField(max_length=1000)

    def to_dict(self, fields):
        data = {}
        for name in fields:
            if name == 'president':
                data[name] = self.president.id
            elif name == 'members':
                data[name] = [member.id for member in self.members.all()]
            else:
                data[name] = self._meta.get_field(name).value_from_object(self)

        return data
    