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
        
        token = response.json()['access_token']
        cls.headers = {'Access': f'Bearer {token}'}
    
        response_user = Client().post('/auth/login', 
                                    data=json.dumps({'id': '20201641', 'password': 'asdf1234'}), 
                                    content_type='application/json')
        user_token = response_user.json()['access_token']
        cls.headers_user = {'Access': f'Bearer {user_token}'}
    

    def test_get_notices(self):
        response = self.client.get('/notice/', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['notices']), 2)
    

    def test_create_notice(self):
        new_notice = {
            "title": "Test notice",
            "content": "This is notice for test",
            "important": True
        }

        response = self.client.post('/notice/', headers=self.headers, data=json.dumps(new_notice), content_type="application/json")
        self.assertEqual(response.status_code, 200)

        id = response.json()['notice']['id']
        notice = Notice.objects.get(id=id)

        self.assertEqual(notice.title, new_notice['title'])
        self.assertEqual(notice.content, new_notice['content'])
        self.assertEqual(notice.important, new_notice['important'])

    
    def test_get_notice(self):
        response = self.client.get('/notice/1', headers=self.headers)
        self.assertEqual(response.status_code, 200)

        id = response.json()['notice']['id']
        notice = Notice.objects.get(id=id)
        
        notice_from_model = Notice.objects.get(id=1)
    
        self.assertEqual(notice.title, notice_from_model.title)
        self.assertEqual(notice.content, notice_from_model.content)
        self.assertEqual(notice.important, notice_from_model.important)
        self.assertEqual(notice.expired, notice_from_model.expired)


    def test_update_notice(self):
        new_notice = {
            "title": "Test notice",
            "content": "This is notice for test",
            "important": True,
            "expired": False
        }

        response = self.client.put('/notice/1', headers=self.headers, data=json.dumps(new_notice), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        
        notice_from_model = Notice.objects.get(id=1)
    
        self.assertEqual(new_notice['title'], notice_from_model.title)
        self.assertEqual(new_notice['content'], notice_from_model.content)
        self.assertEqual(new_notice['important'], notice_from_model.important)
        self.assertEqual(new_notice['expired'], notice_from_model.expired)


    def test_delete_notice(self):
        response_delete = self.client.delete('/notice/1', headers=self.headers)
        self.assertEqual(response_delete.status_code, 200)
        
        response = self.client.get('/notice/', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['notices']), 1)


    def test_unauthorized_member_post(self):
        new_notice = {
            "title": "Test notice",
            "content": "This is notice for test",
            "important": True
        }

        response = self.client.post('/notice/', headers=self.headers_user, data=json.dumps(new_notice), content_type="application/json")
        self.assertEqual(response.status_code, 403)


    def test_unauthorized_member_put(self):
        new_notice = {
            "title": "Test notice",
            "content": "This is notice for test",
            "important": True,
            "expired": False
        }

        response = self.client.put('/notice/1', headers=self.headers_user, data=json.dumps(new_notice), content_type="application/json")
        self.assertEqual(response.status_code, 403)


    def test_unauthorized_member_delete(self):
        response = self.client.delete('/notice/1', headers=self.headers_user)
        self.assertEqual(response.status_code, 403)


    def test_user_get_detail(self):
        response = self.client.get('/notice/1', headers=self.headers_user)
        self.assertEqual(response.status_code, 200)

        id = response.json()['notice']['id']
        notice = Notice.objects.get(id=id)
        
        notice_from_model = Notice.objects.get(id=1)
    
        self.assertEqual(notice.title, notice_from_model.title)
        self.assertEqual(notice.content, notice_from_model.content)
        self.assertEqual(notice.important, notice_from_model.important)
        self.assertEqual(notice.expired, notice_from_model.expired)
