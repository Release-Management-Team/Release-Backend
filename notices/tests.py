import json
from django.test import TestCase, Client

from .models import Notice
from members.models import Member

from tests.data_setup import create_member_data, create_notice_data

class NoticeTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_member_data()
        response = Client().post('/auth/login', 
                                    data=json.dumps({'id': '20231560', 'password': 'asdf5678'}), 
                                    content_type='application/json')
        
        cls.headers = {'Authorization': response.json()['access_token']}

    def setUp(self):
        Notice.objects.all().delete()
        create_notice_data()
    
    def test_getting_notices(self):
        response = self.client.get('/notice/list', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['notices']), 2)
    
    def test_uploading_fcm_token(self):
        token = 'abcde'
        response = self.client.post('/notice/upload-fcm-token', headers=self.headers, data={'fcm_token': token}, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        me = Member.objects.get(id='20231560')
        self.assertEqual(me.fcm_token, token)
        