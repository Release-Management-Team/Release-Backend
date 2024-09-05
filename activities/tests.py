import json
from django.test import TestCase, Client

from .models import Study, Project

class ActivityTestCase(TestCase):
    fixtures = ['members', 'activities']

    @classmethod
    def setUpTestData(cls):
        response = Client().post('/auth/login', 
                                    data=json.dumps({'id': '20231560', 'password': 'asdf5678'}), 
                                    content_type='application/json')
        
        token = response.json()['access_token']
        cls.headers = {'Authorization': f'Bearer {token}'}
    
    def test_getting_studies_prjects(self):
        response = self.client.get('/activity/', headers=self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(len(data['activities']), 3)

    def test_getting_events(self):
        response = self.client.get('/activity/event', headers=self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(len(data['events']), 2)