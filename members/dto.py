from drf_yasg import openapi

# GET
class member_list_dto:
    request = []
    
    response_200 = openapi.Response(
        description="Successful response",
        examples={
            "application/json": {
                "profiles": []
            }
        }
    )

# GET
class member_profile_dto:
    request = [
        openapi.Parameter(
            name='student_id',  # Replace with your parameter name
            in_=openapi.IN_PATH,  # Location of the parameter
            description="ID of the member",
            type=openapi.TYPE_INTEGER  # Replace with the appropriate type
        )
    ]
    
    response_200 = openapi.Response(
        description="Successful response",
        examples={
            "application/json": {
                "id": 1,
                "name": "name",
                "state": "state",
                "role": "role",
                "message": "message",
                "image": "image"
            }
        }
    )

# GET
class get_my_profile_dto:
    request = []
    
    response_200 = openapi.Response(
        description="Successful response",
        examples={
            "application/json": {
                'image': "string",
                'name': "string",
                'role': "string",
                'message': "string",
                'id': 1,
                'department': "string",
                'phone': "string",
                'email': "string",
                'state': "string",
                'joined_semester': "string",
                'new': True,
            }
        }
    )

# PUT
class update_my_profile_dto:
    request = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['phone', 'email', 'message', 'image'],
            properties={
                    'phone': openapi.Schema(type=openapi.TYPE_STRING),
                    'email': openapi.Schema(type=openapi.TYPE_STRING),
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'image': openapi.Schema(type=openapi.TYPE_STRING)
                },
            )
    
    
    response_200 = openapi.Response(
        description="Successful response",
        examples={
            "application/json": {
            }
        }
    )


# POST
class change_password_dto:
    request = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['old_password', 'new_password'],
            properties={
                    'old_password': openapi.Schema(type=openapi.TYPE_STRING),
                    'new_password': openapi.Schema(type=openapi.TYPE_STRING)
                },
            )
    
    response_200 = openapi.Response(
        description="Successful response",
        examples={
            "application/json": {
            }
        }
    )

# POST
class register_device_dto:
    request = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['uuid', 'fcm_token'],
            properties={
                    'uuid': openapi.Schema(type=openapi.TYPE_STRING),
                    'fcm_token': openapi.Schema(type=openapi.TYPE_STRING)
                },
            )
    
    response_200 = openapi.Response(
            description="Success",
            examples={
                "application/json": {
                    "uuid": "string",
                }
            })
   
   
    response_201 = openapi.Response(
            description="Resource created successfully",
            examples={
                "application/json": {
                    "uuid": "string",
                }
            })
   
