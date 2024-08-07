from books.models import Book, BookRecord, BookTag

def create_book_data():
    tag1 = BookTag.objects.create(tag="OS")
    tag2 = BookTag.objects.create(tag="System")
    tag3 = BookTag.objects.create(tag="Math")
    
    book1 = Book(id='1', name='Abstract Algebra An Introduction', author='Thomas W. Hungerford', available=True, image='')
    book1.save()
    book1.tags.add(BookTag.objects.get(tag=tag3))
    book1.save()

    