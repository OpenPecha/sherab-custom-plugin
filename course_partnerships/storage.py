"""
Custom storage backends for course partnerships.
These storage classes read configuration from Django settings that are
configured by the tutor-contrib-s3 plugin.
"""
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class PartnerLogoStorage(S3Boto3Storage):
    """
    Custom S3 storage backend for partner and organization logos.
    Uses configuration from PARTNER_LOGO_BACKEND settings (configured by tutor-contrib-s3).
    """
    
    def __init__(self, **kwargs):
        backend_config = getattr(settings, 'PARTNER_LOGO_BACKEND', {})
        options = backend_config.get('options', {})
        
        kwargs['bucket_name'] = options.get('bucket_name', settings.AWS_STORAGE_BUCKET_NAME)
        kwargs['location'] = options.get('location', 'partner')
        kwargs['querystring_auth'] = options.get('querystring_auth', False)
        
        if 'custom_domain' in options:
            kwargs['custom_domain'] = options['custom_domain']
        
        super().__init__(**kwargs)


class CenterLogoStorage(S3Boto3Storage):
    """
    Custom S3 storage backend for center logos.
    Uses configuration from CENTER_LOGO_BACKEND settings (configured by tutor-contrib-s3).
    """
    
    def __init__(self, **kwargs):
        backend_config = getattr(settings, 'CENTER_LOGO_BACKEND', {})
        options = backend_config.get('options', {})
        
        kwargs['bucket_name'] = options.get('bucket_name', settings.AWS_STORAGE_BUCKET_NAME)
        kwargs['location'] = options.get('location', 'partner/center')
        kwargs['querystring_auth'] = options.get('querystring_auth', False)
        
        if 'custom_domain' in options:
            kwargs['custom_domain'] = options['custom_domain']
        
        super().__init__(**kwargs)


class CourseCreatorStorage(S3Boto3Storage):
    """
    Custom S3 storage backend for course creator profile pictures.
    Uses configuration from COURSE_CREATOR_STORAGE_BACKEND settings (configured by tutor-contrib-s3).
    """
    
    def __init__(self, **kwargs):
        backend_config = getattr(settings, 'COURSE_CREATOR_STORAGE_BACKEND', {})
        options = backend_config.get('options', {})
        
        kwargs['bucket_name'] = options.get('bucket_name', settings.AWS_STORAGE_BUCKET_NAME)
        kwargs['location'] = options.get('location', 'partner/course_creators')
        kwargs['querystring_auth'] = options.get('querystring_auth', False)
        
        if 'custom_domain' in options:
            kwargs['custom_domain'] = options['custom_domain']
        
        super().__init__(**kwargs)
