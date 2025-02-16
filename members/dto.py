from drf_yasg import openapi

member_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
        'name': openapi.Schema(type=openapi.TYPE_STRING),
        'state': openapi.Schema(type=openapi.TYPE_STRING),
        'role': openapi.Schema(type=openapi.TYPE_STRING),
        'message': openapi.Schema(type=openapi.TYPE_STRING),
        'image': openapi.Schema(type=openapi.TYPE_STRING)
    },
    required=['id', 'name', 'state', 'role', 'message', 'image']
)

my_profile_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'image': openapi.Schema(type=openapi.TYPE_STRING),
        'name': openapi.Schema(type=openapi.TYPE_STRING),
        'role': openapi.Schema(type=openapi.TYPE_STRING),
        'message': openapi.Schema(type=openapi.TYPE_STRING),
        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
        'department': openapi.Schema(type=openapi.TYPE_STRING),
        'phone': openapi.Schema(type=openapi.TYPE_STRING),
        'email': openapi.Schema(type=openapi.TYPE_STRING),
        'state': openapi.Schema(type=openapi.TYPE_STRING),
        'joined_semester': openapi.Schema(type=openapi.TYPE_STRING),
        'new': openapi.Schema(type=openapi.TYPE_BOOLEAN),
    },
        
    required=['id', 'name', 'state', 'role', 'message', 'image', 'department', 'phone', 'email', 'joined_semester', 'new']
)


# GET
class member_list_dto:
    request_param = []
    
    response_200 = openapi.Response(
        description="Successful response",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'profiles': openapi.Schema(type=openapi.TYPE_ARRAY, items=member_schema)
            }
        ),
        examples={
            "application/json": {
                "profiles": []
            }
        }
    )

# GET
class member_profile_dto:
    request_param = [
        openapi.Parameter(
            name='student_id',  # Replace with your parameter name
            in_=openapi.IN_PATH,  # Location of the parameter
            description="ID of the member",
            type=openapi.TYPE_INTEGER  # Replace with the appropriate type
        )
    ]
    
    response_200 = openapi.Response(
        description="Successful response",
        schema=member_schema,
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
    request_param = []
    
    response_200 = openapi.Response(
        description="Successful response",
        schema=my_profile_schema,
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
    request_body = openapi.Schema(
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
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={},
            required=[]
        ),
        examples={
            "application/json": {
            }
        }
    )


# POST
class change_password_dto:
    request_body = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['old_password', 'new_password'],
            properties={
                    'old_password': openapi.Schema(type=openapi.TYPE_STRING),
                    'new_password': openapi.Schema(type=openapi.TYPE_STRING)
                },
            )
    
    response_200 = openapi.Response(
        description="Successful response",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={},
            required=[]
        ),
        examples={
            "application/json": {
            }
        }
    )

# POST
class register_device_dto:
    request_body = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['uuid', 'fcm_token'],
            properties={
                    'uuid': openapi.Schema(type=openapi.TYPE_STRING),
                    'fcm_token': openapi.Schema(type=openapi.TYPE_STRING)
                },
            )
    
    response_200 = openapi.Response(
            description="Success",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "uuid": openapi.Schema(type=openapi.TYPE_STRING),
                },
                required=["uuid"]
            ),
            examples={
                "application/json": {
                    "uuid": "string",
                }
            })
   
   
    response_201 = openapi.Response(
            description="Resource created successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "uuid": openapi.Schema(type=openapi.TYPE_STRING),
                },
                required=["uuid"]
            ),
            examples={
                "application/json": {
                    "uuid": "string",
                }
            })
   
