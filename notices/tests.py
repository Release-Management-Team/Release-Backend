import json
from django.test import TestCase, Client

from .models import Notice
from members.models import Member


class NoticeTestCase(TestCase):
    fixtures = ['members', 'notices']

    @classmethod
    def setUpTestData(cls):
        response = Client().post('/auth/login', 
                                    data=json.dumps({'id': '20231560', 'password': 'asdf5678'}), 
                                    content_type='application/json')
        
        cls.headers = {'Authorization': response.json()['access_token']}
    
    def test_getting_notices(self):
        response = self.client.get('/notice/list', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['notices']), 2)
    