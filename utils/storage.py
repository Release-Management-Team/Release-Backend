import minio, base64, hashlib
from django.conf import settings

MINIO_HOST = settings.MINIO_HOST
MINIO_PORT = settings.MINIO_PORT
MINIO_ACCESS_KEY = settings.MINIO_ACCESS_KEY
MINIO_SECRET_KEY = settings.MINIO_SECRET_KEY

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
                endpoint=f'{MINIO_HOST}:{MINIO_PORT}', 
                access_key=MINIO_ACCESS_KEY, 
                secret_key=MINIO_SECRET_KEY, 
                secure=False
            )

def put_base64_image(bucket: str, data: str) -> str:
    client = _get_client()
    data = base64.b64decode(data)
    name = hashlib.md5(data).hexdigest()

    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)
        client.set_bucket_policy(bucket, BUCKET_POLICY)
    client.put_object(bucket_name=bucket, object_name=name, data=data, content_type='image/jpeg')

    return name