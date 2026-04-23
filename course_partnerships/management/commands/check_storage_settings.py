"""
Django management command to check storage backend settings.

Usage:
    ./manage.py lms check_storage_settings
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from course_partnerships.storage import PartnerLogoStorage, CenterLogoStorage, CourseCreatorStorage


class Command(BaseCommand):
    help = 'Check storage backend settings configuration'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== Checking Storage Settings ===\n'))
        
        # Check PARTNER_LOGO_BACKEND
        self.stdout.write('PARTNER_LOGO_BACKEND:')
        partner_backend = getattr(settings, 'PARTNER_LOGO_BACKEND', None)
        if partner_backend:
            self.stdout.write(self.style.SUCCESS(f'  ✓ Configured: {partner_backend}'))
        else:
            self.stdout.write(self.style.ERROR('  ✗ NOT CONFIGURED'))
        
        # Check CENTER_LOGO_BACKEND
        self.stdout.write('\nCENTER_LOGO_BACKEND:')
        center_backend = getattr(settings, 'CENTER_LOGO_BACKEND', None)
        if center_backend:
            self.stdout.write(self.style.SUCCESS(f'  ✓ Configured: {center_backend}'))
        else:
            self.stdout.write(self.style.ERROR('  ✗ NOT CONFIGURED'))
        
        # Check COURSE_CREATOR_STORAGE_BACKEND
        self.stdout.write('\nCOURSE_CREATOR_STORAGE_BACKEND:')
        creator_backend = getattr(settings, 'COURSE_CREATOR_STORAGE_BACKEND', None)
        if creator_backend:
            self.stdout.write(self.style.SUCCESS(f'  ✓ Configured: {creator_backend}'))
        else:
            self.stdout.write(self.style.ERROR('  ✗ NOT CONFIGURED'))
        
        # Check default S3 settings
        self.stdout.write('\n=== Default S3 Settings ===')
        self.stdout.write(f'AWS_STORAGE_BUCKET_NAME: {getattr(settings, "AWS_STORAGE_BUCKET_NAME", "NOT SET")}')
        self.stdout.write(f'AWS_S3_REGION_NAME: {getattr(settings, "AWS_S3_REGION_NAME", "NOT SET")}')
        
        # Test storage instantiation
        self.stdout.write('\n=== Testing Storage Instantiation ===')
        try:
            partner_storage = PartnerLogoStorage()
            self.stdout.write(self.style.SUCCESS(f'✓ PartnerLogoStorage:'))
            self.stdout.write(f'  Bucket: {partner_storage.bucket_name}')
            self.stdout.write(f'  Location: {partner_storage.location}')
            self.stdout.write(f'  Querystring Auth: {partner_storage.querystring_auth}')
            if hasattr(partner_storage, 'custom_domain'):
                self.stdout.write(f'  Custom Domain: {partner_storage.custom_domain}')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ PartnerLogoStorage failed: {e}'))
        
        try:
            center_storage = CenterLogoStorage()
            self.stdout.write(self.style.SUCCESS(f'\n✓ CenterLogoStorage:'))
            self.stdout.write(f'  Bucket: {center_storage.bucket_name}')
            self.stdout.write(f'  Location: {center_storage.location}')
            self.stdout.write(f'  Querystring Auth: {center_storage.querystring_auth}')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ CenterLogoStorage failed: {e}'))
        
        try:
            creator_storage = CourseCreatorStorage()
            self.stdout.write(self.style.SUCCESS(f'\n✓ CourseCreatorStorage:'))
            self.stdout.write(f'  Bucket: {creator_storage.bucket_name}')
            self.stdout.write(f'  Location: {creator_storage.location}')
            self.stdout.write(f'  Querystring Auth: {creator_storage.querystring_auth}')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ CourseCreatorStorage failed: {e}'))
