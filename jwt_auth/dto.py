from drf_yasg import openapi

class login_dto:
    request = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id', 'password'],
            properties={
                    'id': openapi.Schema(type=openapi.TYPE_STRING),
                    'password': openapi.Schema(type=openapi.TYPE_STRING)
                },
            )

    response_200 = openapi.Response(
            description="success",
            examples={
                "application/json": {
                    "access_token": "string",
                    "refresh_token": "string"
                }
            })
    

class refresh_token_dto:
    request = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id', 'password'],
            properties={
                    'id': openapi.Schema(type=openapi.TYPE_STRING),
                    'password': openapi.Schema(type=openapi.TYPE_STRING)
                },
            )
    
    response_200 = openapi.Response(
            description="success",
            examples={
                "application/json": {
                    "access_token": "string",
                    "refresh_token": "string"
                }
            })