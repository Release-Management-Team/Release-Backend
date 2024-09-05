import json
from django.test import TestCase, Client

from members.models import Member

class NotificationTestCase(TestCase):
    fixtures = ['members']

    @classmethod
    def setUpTestData(cls):
        response = Client().post('/auth/login', 
                                    data=json.dumps({'id': '20231560', 'password': 'asdf5678'}), 
                                    content_type='application/json')
        
        token = response.json()['access_token']
        cls.headers = {'Authorization': f'bearer {token}'}
    

    def test_uploading_fcm_token(self):
            token = 'abcde'
            response = self.client.post('/notification/upload-fcm-token', headers=self.headers, data={'fcm_token': token}, content_type='application/json')
            self.assertEqual(response.status_code, 200)

            me = Member.objects.get(id='20231560')
            self.assertEqual(me.fcm_token, token)
            