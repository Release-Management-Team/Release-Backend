from django.test import TestCase
import json

from .models import Book, BookRecord, BookTag

class BookTestCase(TestCase):
    def setUp(self):
        BookTag.objects.create(tag='System')
        BookTag.objects.create(tag='OS')
        
        Book.objects.create(id='1', name='test book 1', author='신현수', available=True, image='')
        Book.objects.create(id='2', name='test book 2', author='정재헌', available=False, image='')
        
    def test_book_list(self):
        response = self.client.get('/books/book-list')
        self.assertIs(response.status_code, 200)
        
        body = json.loads(response.content)
        print(body)
        self.assertTrue(body == {'books': [{'id': '1', 'name': 'test book 1', 'available': True, 'image': ''}, {'id': '2', 'name': 'test book 2', 'available': False, 'image': ''}]})
    
    def test_book_info(self):
        pass