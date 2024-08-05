from django.test import TestCase
import json

from members.models import Member, State, Role

# id          = models.IntegerField(primary_key=True)
# name        = models.CharField(max_length=10)
# password    = models.BinaryField(max_length=100) # byte array encrypted by bcrpyt
# fcm_token   = models.CharField(null=True)
# phone       = models.CharField(max_length=20)
# email       = models.EmailField()
# state       = models.IntegerField(choices=State.choices)
# role        = models.IntegerField(choices=Role.choices)
# message     = models.CharField(max_length=300)
# image       = models.CharField(max_length=10)

# Create your tests here.
class AccountTestCase(TestCase):
    def setUp(self):
        Member.objects.create(id='20201641', name='정재헌', password='asdf1234', phone='01000000000', email='test1@gmail.com', state=State.ENROLLED, Role=Role.STAFF, message='', image='')
        Member.objects.create(id='20231560', name='신현수', password='qwer1234', phone='01000000001', email='test2@gmail.com', state=State.ENROLLED, Role=Role.STAFF, message='', image='')

    # def test_validate_access(self):
    #     response = self.client.get('/accounts/validate_access')
    #     self.assertIs(response.status_code, 200)
        
    #     body = json.loads(response.content)
    #     print(body)
    #     self.assertTrue(body == {'books': [{'id': '1', 'name': 'test book 1', 'available': True, 'image': ''}, {'id': '2', 'name': 'test book 2', 'available': False, 'image': ''}]})