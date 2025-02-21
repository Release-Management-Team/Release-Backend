from drf_yasg import openapi

book_schema = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'availability': openapi.Schema(type=openapi.TYPE_STRING),
                'author': openapi.Schema(type=openapi.TYPE_STRING),
                'tags': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                'image': openapi.Schema(type=openapi.TYPE_STRING)
            },
            required=['id', 'title', 'availability', 'author', 'image']
        )

# GET
class get_book_list_dto:
    request_param = []
    
    response_200 = openapi.Response(
        description="Successful response",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'books': openapi.Schema(type=openapi.TYPE_ARRAY, items=book_schema)
            },
            required=[]
        ),
        examples={
            "application/json": {
                "books": []
            }
        }
    )


# GET
class get_book_detail_dto:
    request_param = [
        openapi.Parameter(
            name="book_id",
            in_=openapi.IN_PATH,
            type=openapi.TYPE_INTEGER,
            required=True,
            description="book id"
        )
    ]
    
    response_200 = openapi.Response(
        description="Successful response",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "book": book_schema
            },
            required=["book"]
        ),
        examples={
            "application/json": {
                "id": 1,
                "title": "string",
                "availability": "string",
                "available_date": "string",
                "author": "string",
                "tags": [
                    "string"
                ],
                "image": "string"
            }
        }
    )


# POST
class borrow_book_dto:
    request_param = [
        openapi.Parameter(
            name="book_id",
            in_=openapi.IN_PATH,
            type=openapi.TYPE_INTEGER,
            required=True,
            description="book id"
        )
    ]
    
    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'qrcode': openapi.Schema(type=openapi.TYPE_STRING)
        },
        required=['qrcode']
    )

    response_200 = openapi.Response(
        description="Successful response",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={},
            required=[]
        ),
        examples={
            "application/json": {}
        }
    )


# POST
class return_book_dto:
    request_param = [
        openapi.Parameter(
            name="book_id",
            in_=openapi.IN_PATH,
            type=openapi.TYPE_INTEGER,
            required=True,
            description="book id"
        )
    ]
    
    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'qrcode': openapi.Schema(type=openapi.TYPE_STRING)
        },
        required=['qrcode']
    )

    response_200 = openapi.Response(
        description="Successful response",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={},
            required=[]
        ),
        examples={
            "application/json": {}
        }
    )


# GET
class get_borrowed_books_dto:
    request_param = []
    
    response_200 = openapi.Response(
        description="Successful response",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "books": openapi.Schema(type=openapi.TYPE_ARRAY, items=book_schema)
            },
            required=[]
        ),
        examples={
            "application/json": {
                "books": []
            }
        }
    )