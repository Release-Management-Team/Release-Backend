from drf_yasg import openapi

# GET
class get_notice_list_dto:
    request_param = []
    
    response_200 = openapi.Response(
        description="Successful response",
        examples={
            "application/json": {
                "notices": [{
                    "id": "int",
                    "title": "string",
                    "content": "string",
                    "date": "string",
                    "important": "string",
                    "expired": "bool"
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
        examples={
            "application/json": {
                "id": "int",
                "title": "string",
                "content": "string",
                "date": "string",
                "important": "string",
                "expired": "bool"
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
        examples={
            "application/json": {
                "notice": {
                    "id": 1,
                    "title": "title",
                    "content": "content",
                    "date": "date",
                    "important": "important",
                    "expired": "expired"
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
        examples={
            "application/json": {}
        }
    )