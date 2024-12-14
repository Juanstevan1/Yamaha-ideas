from google.cloud import storage
from datetime import timedelta

def generate_signed_url(bucket_name, object_name, expiration_minutes=15):
    """
    Genera una URL firmada para acceso temporal a un objeto de GCP Storage.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    url = blob.generate_signed_url(
        expiration=timedelta(minutes=expiration_minutes),
        method="GET"
    )

    return url
