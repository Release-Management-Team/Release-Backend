import json, bcrypt

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
        self.assertEqual('20201641', json_response.get('id'))
        self.assertEqual('정재헌', json_response.get('name'))
        self.assertEqual('01000000000', json_response.get('phone'))
        self.assertEqual('test0@gmail.com', json_response.get('email'))
        

    def test_update_my_profile(self):
        print('\nTesting update_my_profile...')
        data = {
            'phone': '01012345678',
            'email': 'deadbeaf@gmail.com',
            'message': 'you cracked',
            'image': 'imagine'
        }
        response = self.client.post('/members/update-profile', headers=self.headers, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        member = Member.objects.get(id='20201641')
        self.assertEqual(member.phone, '01012345678')
        self.assertEqual(member.email, 'deadbeaf@gmail.com')
        self.assertEqual(member.message, 'you cracked')
        self.assertEqual(member.image, 'imagine')


    def test_change_password(self):
        print('\nTesting change_password...')

        new_password = 'new_password'
        data = {
            'password': new_password
        }
        response = self.client.post('/members/change-password', headers=self.headers, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        member = Member.objects.get(id='20201641')
        self.assertTrue(bcrypt.checkpw(new_password.encode('utf-8'), member.password.tobytes()))



    def test_get_members_list(self):
        print('\nTesting get_members_list...')

        response = self.client.get('/members/member-list', headers=self.headers)
        json_response = response.json()
        profiles = json_response.get('profiles')
        for i in profiles:
            print(i)


    def test_get_member_profile(self):
        print('\nTesting get_member_profile...')

        id = '20231560'
        data = {
            'id': '20231560'
        }
        response = self.client.get('/member/member-profile', headers=self.headers, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        json_response = response.json()
        member = Member.objects.values('id', 'name', 'state', 'role', 'message', 'image')
        
        print(json_response)
        print(member)
        
        