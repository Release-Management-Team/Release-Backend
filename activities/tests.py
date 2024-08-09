import json
from django.test import TestCase, Client

from .models import Study, Project

from tests.data_setup import create_member_data
from tests.data_setup.activity_setup import create_activity_data

class ActivityTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_member_data()
        response = Client().post('/auth/login', 
                                    data=json.dumps({'id': '20231560', 'password': 'asdf5678'}), 
                                    content_type='application/json')
        cls.headers = {'Authorization': response.json()['access_token']}

    def setUp(self):
        create_activity_data()
    
    def test_getting_studies(self):
        response = self.client.get('/activity/studies', headers=self.headers)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        print(data)
        self.assertEqual(len(data['studies']), 2)

    def test_getting_projects(self):
        response = self.client.get('/activity/projects', headers=self.headers)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(len(data['projects']), 0)