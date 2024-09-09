import json, bcrypt, requests

from django.test import TestCase
from django.conf import settings

from .models import Member

from utils.encryption import checkpw

# Create your tests here.
class MemberTestCase(TestCase):
    fixtures = ['members', 'notices', 'activities']

    def setUp(self):
        data = {
            'id': '20201641',
            'password': 'asdf1234'
        }
        response = self.client.post('/auth/login', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        token = json_response.get('access_token')        
        self.headers = {
            'Access': f'Bearer {token}'
        }

    def test_home(self):
        response = self.client.get('/member/home', headers=self.headers)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data['name'], '정재헌')
        self.assertEqual(data['image'], '')
        self.assertEqual(len(data['notices']), 1)
        self.assertEqual(len(data['schedules'][4]), 1)


    def test_get_my_profile(self):
        # print('\nTesting get_my_profile...')

        response = self.client.get('/member/profile', headers=self.headers)
        self.assertEqual(response.status_code, 200)

        json_response = response.json()
        self.assertEqual('20201641', json_response.get('id'))
        self.assertEqual('정재헌', json_response.get('name'))
        self.assertEqual('01000000000', json_response.get('phone'))
        self.assertEqual('test0@gmail.com', json_response.get('email'))
        

    def test_update_my_profile(self):
        # print('\nTesting update_my_profile...')
        data = {
            'phone': '01012345678',
            'email': 'deadbeaf@gmail.com',
            'message': 'you cracked',
            'image': 'dGVzdCBpbWFnZQ==' if settings.TEST_STORAGE else ''
        }
        response = self.client.post('/member/profile/update', headers=self.headers, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/member/profile', headers=self.headers, content_type='application/json')

        member = response.json()
        self.assertEqual(member['phone'], '01012345678')
        self.assertEqual(member['email'], 'deadbeaf@gmail.com')
        self.assertEqual(member['message'], 'you cracked')

        if settings.TEST_STORAGE:
            image_url = member['image']
            image = requests.get(image_url)
            self.assertEqual(image.content, b'test image')
        

    def test_change_password(self):
        # print('\nTesting change_password...')

        old_password = 'asdf1234'
        new_password = 'new_password1'
        data = {
            'old_password': old_password,
            'new_password': new_password
        }
        response = self.client.post('/member/change-password', headers=self.headers, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        member = Member.objects.get(id='20201641')
        self.assertTrue(checkpw(new_password, member.password))


    def test_change_password_wrong_pw(self):
        # print('\nTesting change_password wit...')

        old_password = 'qwer1234'
        new_password = 'new_password'
        data = {
            'old_password': old_password,
            'new_password': new_password
        }
        response = self.client.post('/member/change-password', headers=self.headers, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)



    def test_get_members_list(self):
        # print('\nTesting get_members_list...')

        response = self.client.get('/member/member-list', headers=self.headers)
        json_response = response.json()
        profiles = json_response.get('profiles')
        


    def test_get_member_profile(self):
        # print('\nTesting get_member_profile...')

        id = '20231560'
        response = self.client.get('/member/member-profile?id=20231560', headers=self.headers)
        self.assertEqual(response.status_code, 200)

        json_response = response.json()
        member = Member.objects.get(id=id)
        
        self.assertEqual(member.id, json_response.get('id'))
        self.assertEqual(member.name, json_response.get('name'))
        self.assertEqual(member.message, json_response.get('message'))
        self.assertEqual(member.image, json_response.get('image'))
        self.assertEqual(member.state, json_response.get('state'))
        self.assertEqual(member.role, json_response.get('role'))
        
        