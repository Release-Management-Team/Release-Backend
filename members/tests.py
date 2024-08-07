import json

from django.test import TestCase

from tests.data_setup import *

from .models import Member

# Create your tests here.
class MemberTestCase(TestCase):
    def setUp(self):
        Member.objects.all().delete()
        create_member_data()
        data = {
            'id': '20201641',
            'password': 'asdf1234'
        }
        response = self.client.post('/auth/login', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        token = json_response.get('access_token')        
        self.headers = {
            'Authorization': token
        }


    def test_get_my_profile(self):
        print('\nTesting get_my_profile...')
        response = self.client.get('/members/my-profile', headers=self.headers)
        self.assertEqual(response.status_code, 200)

        json_response = response.json()
        self.assertEqual(20201641, json_response.get('id'))
        self.assertEqual('정재헌', json_response.get('name'))
        self.assertEqual('01000000000', json_response.get('phone'))
        self.assertEqual('test0@gmail.com', json_response.get('email'))
        

    def test_update_my_profile(self):
        print('\nTesting update_my_profile...')
        pass


    def test_change_password(self):
        print('\nTesting change_password...')
        pass


    def test_get_members_list(self):
        print('\nTesting get_members_list...')
        response = self.client.get('/members/member-list', headers=self.headers)
        json_response = response.json()
        profiles = json_response.get('profiles')
        for i in profiles:
            print(i)

        
    def test_get_member_profile(self):
        print('\nTesting get_member_profile...')
        pass
        