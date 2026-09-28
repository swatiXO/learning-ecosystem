"""Pre-signed object storage URLs. MinIO in dev, S3 in prod (PROJECT.md §4) - both speak
the same S3 API, so boto3 works against either. Signing is local (HMAC over the request),
not a network call, so this never needs to actually reach the storage backend.
"""

import boto3
from botocore.client import Config as BotoConfig
from botocore.exceptions import ClientError

from app.config import settings

# Returned by MinIO/S3 when the bucket is already there - the only "failures" we expect
# and want to swallow when ensuring it exists.
_BUCKET_ALREADY_EXISTS_CODES = {"BucketAlreadyOwnedByYou", "BucketAlreadyExists"}

# Long enough for a mobile client on a slow connection to start the upload, short enough
# that a leaked URL isn't usable for long.
DEFAULT_UPLOAD_URL_EXPIRY_SECONDS = 300


def _client():
    return boto3.client(
        "s3",
        endpoint_url=f"http://{settings.minio_endpoint}",
        aws_access_key_id=settings.minio_root_user,
        aws_secret_access_key=settings.minio_root_password,
        region_name="us-east-1",
        config=BotoConfig(signature_version="s3v4"),
    )


def ensure_bucket_exists() -> None:
    """Idempotent - safe to call every app startup. Docker Compose only starts the MinIO
    server; nothing else provisions the bucket (and neither `minio/mc` nor `minio/minio`
    itself currently pull from Docker Hub in this environment, so a compose-level
    bootstrap container isn't reliable here either)."""
    client = _client()
    try:
        client.create_bucket(Bucket=settings.minio_bucket)
    except ClientError as exc:
        if exc.response.get("Error", {}).get("Code") not in _BUCKET_ALREADY_EXISTS_CODES:
            raise


def presigned_upload_url(
    storage_key: str, expires_in: int = DEFAULT_UPLOAD_URL_EXPIRY_SECONDS
) -> str:
    return _client().generate_presigned_url(
        "put_object",
        Params={"Bucket": settings.minio_bucket, "Key": storage_key},
        ExpiresIn=expires_in,
    )
