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
        
        token = response.json()['access_token']
        cls.headers = {'Authorization': f'Bearer {token}'}
        
    def test_getting_book_list(self):
        response = self.client.get('/book/', headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_getting_book_info(self):
        response = self.client.get('/book/info?id=1' , headers=self.headers)
        data = response.json()
        self.assertEqual(data['title'], 'Operating System Concept')
        self.assertEqual(response.status_code, 200)

    def test_borrow_return(self):
        response = self.client.post('/book/borrow', headers=self.headers, data={'id': '2', 'qrcode': settings.QRCODE}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Book.objects.get(id='2').availability, 'rented')

        response = self.client.post('/book/return', headers=self.headers, data={'id': '2', 'qrcode': settings.QRCODE}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Book.objects.get(id='2').availability, 'available')

    def test_borrowing_book_with_invalid_qr(self):
        response = self.client.post('/book/borrow', headers=self.headers, data={'id': '2', 'qrcode': settings.QRCODE + 'a'}, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        body = response.json()
        self.assertEqual(body['error'], 'ERR_INVALID_QR')

    def test_borrowing_unavailble_book(self):
        response = self.client.post('/book/borrow', headers=self.headers, data={'id': '1', 'qrcode': settings.QRCODE}, content_type='application/json')
        self.assertEqual(response.json()['error'], 'ERR_UNABLE_TO_BORROW')

    def test_borrowing_invalid_book(self):
        response = self.client.post('/book/borrow', headers=self.headers, data={'id': '10', 'qrcode': settings.QRCODE}, content_type='application/json')
        self.assertEqual(response.json()['error'], 'ERR_INVALID_BOOK_ID')

    def test_getting_borrowed_books1(self):
        response = self.client.get('/book/borrowing', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['books'], [])

    def test_getting_borrowed_books1(self):
        self.client.post('/book/borrow', headers=self.headers, data={'id': '2', 'qrcode': settings.QRCODE}, content_type='application/json')

        response = self.client.get('/book/borrowing', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['books']), 1)
        self.assertEqual(data['books'][0]['id'], '2')

        self.client.post('/book/return', headers=self.headers, data={'id': '2', 'qrcode': settings.QRCODE}, content_type='application/json')

        