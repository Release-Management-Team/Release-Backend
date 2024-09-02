from django.db import models

class State:
    ENROLLED  = 0
    ABSENCE   = 1
    GRADUATED = 2
    choices   = (
        (ENROLLED,  '재학'),
        (ABSENCE,   '휴학'),
        (GRADUATED, '졸업'),
    )

class Role:
    MEMBER  = 0
    STAFF   = 1
    choices = (
        (MEMBER, '학회원'),
        (STAFF,  '임원'),
    )
    

class Member(models.Model):
    id          = models.CharField(primary_key=True, max_length=12)
    name        = models.CharField(max_length=10)
    password    = models.BinaryField(max_length=100) # byte array encrypted by bcrpyt
    fcm_token   = models.CharField(max_length=200, blank=True)
    department  = models.CharField(max_length=100)
    phone       = models.CharField(max_length=20)
    email       = models.EmailField()
    state       = models.IntegerField(choices=State.choices)
    role        = models.IntegerField(choices=Role.choices)
    message     = models.CharField(max_length=300, blank=True)
    image       = models.CharField(max_length=32, blank=True)
    joined_semester = models.CharField(max_length=10)
    new         = models.BooleanField()
