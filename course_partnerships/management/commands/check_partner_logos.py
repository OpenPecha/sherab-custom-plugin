"""
Django management command to check where partner logos are stored.

Usage:
    ./manage.py lms check_partner_logos
"""
from django.core.management.base import BaseCommand
from course_partnerships.models import Partner, Center, CourseCreator


class Command(BaseCommand):
    help = 'Check where partner logos are currently stored'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== Partner Logos ===\n'))
        
        partners = Partner.objects.all()
        for partner in partners:
            self.stdout.write(f'Partner: {partner.name}')
            if partner.logo:
                self.stdout.write(f'  Logo path: {partner.logo.name}')
                self.stdout.write(f'  Logo URL: {partner.logo.url}')
                self.stdout.write(f'  Storage: {partner.logo.storage.__class__.__name__}')
                self.stdout.write(f'  Bucket: {partner.logo.storage.bucket_name}')
            else:
                self.stdout.write('  No logo')
            
            if partner.banner:
                self.stdout.write(f'  Banner path: {partner.banner.name}')
                self.stdout.write(f'  Banner URL: {partner.banner.url}')
            self.stdout.write('')
        
        self.stdout.write(self.style.SUCCESS('\n=== Center Logos ===\n'))
        centers = Center.objects.all()
        for center in centers:
            self.stdout.write(f'Center: {center.name}')
            if center.logo:
                self.stdout.write(f'  Logo path: {center.logo.name}')
                self.stdout.write(f'  Logo URL: {center.logo.url}')
            else:
                self.stdout.write('  No logo')
            self.stdout.write('')
        
        self.stdout.write(self.style.SUCCESS('\n=== Course Creators ===\n'))
        creators = CourseCreator.objects.all()
        for creator in creators:
            self.stdout.write(f'Creator: {creator.name}')
            if creator.profile_picture:
                self.stdout.write(f'  Profile path: {creator.profile_picture.name}')
                self.stdout.write(f'  Profile URL: {creator.profile_picture.url}')
            else:
                self.stdout.write('  No profile picture')
            self.stdout.write('')
