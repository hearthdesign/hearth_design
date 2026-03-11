from storages.backends.s3boto3 import S3Boto3Storage

class SupabaseBackupsStorage(S3Boto3Storage):
    bucket_name = "backup"
