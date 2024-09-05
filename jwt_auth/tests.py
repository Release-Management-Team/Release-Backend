from django.test import TestCase

from members.models import Member, State, Role
from django.conf import settings
from .tokens import *
import json

from utils.encryption import hashpw

class AccountTestCase(TestCase):
    fixtures = ['members']

    def test_validate_access(self):
        access_token = create_access_token('20201641')
        headers = {
            'Authorization': f'bearer {access_token}'
        }
        response = self.client.get('/auth/validate-access', headers=headers)
        self.assertEqual(response.status_code, 200)


    def test_refresh_token(self):
        access_token = create_access_token('20201641')
        refresh_token = create_refresh_token()
        headers = {
            'Authorization': f'bearer {access_token}',
            'X-Refresh_Token': refresh_token
        }
        response = self.client.get('/auth/refresh-token', headers=headers)
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        
        try:
            jwt.decode(payload['access_token'], settings.SECRET_KEY, algorithms='HS256')
        except:
            print('wrong access token')
            return
        
        try:
            jwt.decode(payload['refresh_token'], settings.SECRET_KEY, algorithms='HS256')
        except:
            print('wrong refresh token')
            return
        

    def test_login(self):
        data = {
            'id': '20201641',
            'password': 'asdf1234'
        }
        response = self.client.post('/auth/login', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    
    def test_login_wrong_id(self):
        data = {
            'id': '20201642',
            'password': 'asdf1234'
        }
        response = self.client.post('/auth/login', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 401)
    
    
    def test_login_wrong_password(self):
        data = {
            'id': '20201641',
            'password': 'asdf1235'
        }
        response = self.client.post('/auth/login', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 401)