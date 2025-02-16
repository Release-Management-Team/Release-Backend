from drf_yasg import openapi


#GET
class validate_access_dto:
    request_param = []

    response_200 = openapi.Response(
            description="success",
            examples={
                "application/json": {}
            })


#POST
class login_dto:
    request_body = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id', 'password'],
            properties={
                    'id': openapi.Schema(type=openapi.TYPE_STRING),
                    'password': openapi.Schema(type=openapi.TYPE_STRING)
                },
            )

    response_200 = openapi.Response(
            description="success",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                    'refresh_token': openapi.Schema(type=openapi.TYPE_STRING)
                },
                required=['access_token', 'refresh_token']
            ),
            examples={
                "application/json": {
                    "access_token": "string",
                    "refresh_token": "string"
                }
            })
    

#GET
class refresh_token_dto:
    request_param = []
    
    response_200 = openapi.Response(
            description="success",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                    'refresh_token': openapi.Schema(type=openapi.TYPE_STRING)
                },
                required=['access_token', 'refresh_token']
            ),
            examples={
                "application/json": {
                    "access_token": "string",
                    "refresh_token": "string"
                }
            })