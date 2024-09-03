from io import BytesIO
import minio, base64
from django.conf import settings

STORAGE_HOST = settings.STORAGE_HOST
STORAGE_ACCESS_KEY = settings.STORAGE_ACCESS_KEY
STORAGE_SECRET_KEY = settings.STORAGE_SECRET_KEY

BUCKET_POLICY = """
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "*"
                ]
            },
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::*"
            ]
        }
    ]
}
"""

def _get_client() -> minio.Minio:
    return minio.Minio(
                endpoint=f'{STORAGE_HOST}', 
                access_key=STORAGE_ACCESS_KEY, 
                secret_key=STORAGE_SECRET_KEY, 
                secure=False
            )

def put_base64_image(bucket: str, data: str, name: str):
    client = _get_client()
    data = base64.b64decode(data)

    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)
        client.set_bucket_policy(bucket, BUCKET_POLICY)
    client.put_object(bucket_name=bucket, object_name=name, data=BytesIO(data), length=len(data), content_type='image/jpeg')
