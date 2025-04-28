from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class BaseS3Storage(S3Boto3Storage):
    """Base storage backend for S3."""

    bucket_name = settings.AWS_PRIVATE_STORAGE_BUCKET_NAME
    querystring_auth = True
    querystring_expire = 3600
    file_overwrite = False

    def url(self, name, parameters=None, expire=None, http_method=None):
        """Redefine url. For clustered S3 use two different endpoints:
        - INTERNAL: `settings.AWS_S3_ENDPOINT_URL` - for internal operations
        - EXTERNAL: `settings.AWS_S3_EXTERNAL_ENDPOINT_URL` - for external API requests
        """
        url = super().url(name, parameters, expire, http_method)
        if (
            hasattr(settings, "AWS_S3_EXTERNAL_ENDPOINT_URL")
            and settings.AWS_S3_EXTERNAL_ENDPOINT_URL != settings.AWS_S3_ENDPOINT_URL
        ):
            url = url.replace(
                settings.AWS_S3_ENDPOINT_URL, settings.AWS_S3_EXTERNAL_ENDPOINT_URL
            )

        return url


class S3StaticCloudStorage(BaseS3Storage):
    """Storage backend for static files."""

    location = "static"
    file_overwrite = True
    default_acl = "public-read"
    bucket_name = settings.AWS_STATIC_STORAGE_BUCKET_NAME
    querystring_auth = False


class S3MediaCloudStorage(BaseS3Storage):
    """Storage backend for media files."""

    location = "media"
    default_acl = "public-read"
