from drf_yasg import openapi


notice_schema = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the notice'),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Title of the notice'),
                'content': openapi.Schema(type=openapi.TYPE_STRING, description='Content of the notice'),
                'date': openapi.Schema(type=openapi.TYPE_STRING, description='Date of the notice(format example: 2025-02-21 13:41:08.477574+00:00)'),
                'important': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Importance of the notice'),
                'expired': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Whether the notice is expired')
            },
            required=['id', 'title', 'content', 'date', 'important', 'expired']
        )


# GET
class get_notice_list_dto:
    request_param = []
    
    response_200 = openapi.Response(
        description="Successful response",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'notices': openapi.Schema(type=openapi.TYPE_ARRAY, items=notice_schema)
            }
        ),
        examples={
            "application/json": {
                "notices": [{
                    "id": 1,
                    "title": "title",
                    "content": "content",
                    "date": "date",
                    "important": "important",
                    "expired": "expired"
                }]
            }
        }
    )


# POST
class create_notice_dto:
    request_param = []

    request_body = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Title of the notice'),
                'content': openapi.Schema(type=openapi.TYPE_STRING, description='Content of the notice'),
                'important': openapi.Schema(type=openapi.TYPE_STRING, description='Importance of the notice'),
            },
            required=['title', 'content', 'important']
        )
    
    response_200 = openapi.Response(
        description="Successful response",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'notice': notice_schema
            },
            required=['notice']
        ),
        examples={
            "application/json": {
                "notice": {
                    "id": "int",
                    "title": "string",
                    "content": "string",
                    "date": "string",
                    "important": "string",
                    "expired": "bool"
                }
            }
        }
    )


# GET
class get_notice_dto:
    request_param = [
        openapi.Parameter(
            name='notice_id',  # Replace with your parameter name
            in_=openapi.IN_PATH,  # Location of the parameter
            description="ID of the notice",
            type=openapi.TYPE_INTEGER  # Replace with the appropriate type
        )
    ]
    
    response_200 = openapi.Response(
        description="Successful response",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'notice': notice_schema
            },
            required=['notice']
        ),
        examples={
            "application/json": {
                "notice": {
                    "id": "int",
                    "title": "string",
                    "content": "string",
                    "date": "string",
                    "important": "string",
                    "expired": "bool"
                }   
            }
        }
    )


# PUT
class update_notice_dto:
    request_param = [
        openapi.Parameter(
            name='notice_id',
            in_=openapi.IN_PATH,
            description="ID of the notice",
            type=openapi.TYPE_INTEGER
        )
    ]
        
    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, description='Title of the notice'),
            'content': openapi.Schema(type=openapi.TYPE_STRING, description='Content of the notice'),
            'important': openapi.Schema(type=openapi.TYPE_STRING, description='Importance of the notice'),
        },
        required=['title', 'content', 'important']
    )

    response_200 = openapi.Response(
        description="Successful response",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'notice': notice_schema
            },
            required=['notice']
        ),
        examples={
            "application/json": {
                "notice": {
                    "id": "int",
                    "title": "string",
                    "content": "string",
                    "date": "string",
                    "important": "string",
                    "expired": "bool"
                }   
            }
        }
    )


# DELETE
class delete_notice_dto:
    request_param = [
        openapi.Parameter(
            name='notice_id',
            in_=openapi.IN_PATH,
            description="ID of the notice",
            type=openapi.TYPE_INTEGER
        )
    ]

    response_200 = openapi.Response(
        description="Successful response",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={}
        ),
        examples={
            "application/json": {}
        }
    )


class get_important_notice_list_dto:
    request_param = []
    


    response_200 = openapi.Response(
        description="Successful response",
        schema=openapi.Schema(
            type=openapi.TYPE_ARRAY, 
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the notice'),
                            'title': openapi.Schema(type=openapi.TYPE_STRING, description='Title of the notice'),
                        },
                required=['id', 'title']
            )),

        examples={
            "application/json": [{
                "id": 1,
                "title": "title1",
            },
            {
                "id": 2,
                "title": "title2",
            }]
        }
    )
