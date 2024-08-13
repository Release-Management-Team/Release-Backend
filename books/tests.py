import json
from django.test import TestCase, Client
from django.conf import settings

from .models import Book, BookRecord, BookTag

class BookTestCase(TestCase):
    fixtures = ['members', 'books']

    @classmethod
    def setUpTestData(cls):
        response = Client().post('/auth/login', 
                                    data=json.dumps({'id': '20231560', 'password': 'asdf5678'}), 
                                    content_type='application/json')
        cls.headers = {'Authorization': response.json()['access_token']}
        
    def test_getting_book_list(self):
        response = self.client.get('/book/list', headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_getting_book_info(self):
        response = self.client.get('/book/info?id=1' , headers=self.headers)
        self.assertEqual(response.status_code, 200)
    
    def test_borrowing_book(self):
        response = self.client.post('/book/borrow', headers=self.headers, data={'id': '1', 'qrcode': settings.QRCODE}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
   
        book = Book.objects.get(id='1')
        self.assertFalse(book.available)

    def test_returning_book(self):
        self.client.post('/book/borrow', headers=self.headers, data={'id': '1', 'qrcode': settings.QRCODE}, content_type='application/json')
        response = self.client.post('/book/return', headers=self.headers, data={'id': '1', 'qrcode': settings.QRCODE}, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        book = Book.objects.get(id='1')
        self.assertTrue(book.available)
        
    def test_returning_invalid_book(self):
        response = self.client.post('/book/return', headers=self.headers, data={'id': '1', 'qrcode': settings.QRCODE}, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_getting_borrowing_books(self):
        response = self.client.post('/book/borrow', headers=self.headers, data={'id': '1', 'qrcode': settings.QRCODE}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/book/borrowing', headers=self.headers)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(len(data['books']), 1)