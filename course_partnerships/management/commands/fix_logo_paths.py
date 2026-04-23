"""
Django management command to fix partner logo paths in database.

Removes duplicate path segments caused by old file paths.

Usage:
    ./manage.py lms fix_logo_paths --dry-run
    ./manage.py lms fix_logo_paths
"""
from django.core.management.base import BaseCommand
from course_partnerships.models import Partner, Center, CourseCreator


class Command(BaseCommand):
    help = 'Fix partner/center logo paths in database to remove duplicate segments'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be changed without actually doing it',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made\n'))
        
        total_fixed = 0
        
        # Fix Partner logos and banners
        self.stdout.write(self.style.SUCCESS('=== Fixing Partner Logos ===\n'))
        total_fixed += self.fix_partner_fields(Partner, dry_run)
        
        # Fix Center logos and banners
        self.stdout.write(self.style.SUCCESS('\n=== Fixing Center Logos ===\n'))
        total_fixed += self.fix_center_fields(Center, dry_run)
        
        # Fix CourseCreator profile pictures
        self.stdout.write(self.style.SUCCESS('\n=== Fixing Course Creator Profiles ===\n'))
        total_fixed += self.fix_creator_fields(CourseCreator, dry_run)
        
        if dry_run:
            self.stdout.write(self.style.WARNING(f'\nDRY RUN COMPLETE - Would fix {total_fixed} fields'))
        else:
            self.stdout.write(self.style.SUCCESS(f'\nFIXED {total_fixed} fields'))

    def fix_partner_fields(self, model_class, dry_run):
        """Fix Partner logo and banner paths."""
        fixed = 0
        
        for partner in model_class.objects.all():
            self.stdout.write(f'Partner: {partner.name}')
            
            # Fix logo
            if partner.logo and partner.logo.name:
                old_path = partner.logo.name
                new_path = self.clean_path(old_path, 'logos/')
                
                if old_path != new_path:
                    self.stdout.write(f'  Logo: {old_path} -> {new_path}')
                    if not dry_run:
                        partner.logo.name = new_path
                        fixed += 1
                else:
                    self.stdout.write(f'  Logo: OK ({old_path})')
            
            # Fix banner
            if partner.banner and partner.banner.name:
                old_path = partner.banner.name
                new_path = self.clean_path(old_path, 'banners/')
                
                if old_path != new_path:
                    self.stdout.write(f'  Banner: {old_path} -> {new_path}')
                    if not dry_run:
                        partner.banner.name = new_path
                        fixed += 1
                else:
                    self.stdout.write(f'  Banner: OK ({old_path})')
            
            if not dry_run and (partner.logo or partner.banner):
                partner.save()
            
            self.stdout.write('')
        
        return fixed

    def fix_center_fields(self, model_class, dry_run):
        """Fix Center logo and banner paths."""
        fixed = 0
        
        for center in model_class.objects.all():
            self.stdout.write(f'Center: {center.name}')
            
            # Fix logo
            if center.logo and center.logo.name:
                old_path = center.logo.name
                new_path = self.clean_path(old_path, 'logos/', prefix='center/')
                
                if old_path != new_path:
                    self.stdout.write(f'  Logo: {old_path} -> {new_path}')
                    if not dry_run:
                        center.logo.name = new_path
                        fixed += 1
                else:
                    self.stdout.write(f'  Logo: OK ({old_path})')
            
            # Fix banner
            if center.banner and center.banner.name:
                old_path = center.banner.name
                new_path = self.clean_path(old_path, 'banners/', prefix='center/')
                
                if old_path != new_path:
                    self.stdout.write(f'  Banner: {old_path} -> {new_path}')
                    if not dry_run:
                        center.banner.name = new_path
                        fixed += 1
                else:
                    self.stdout.write(f'  Banner: OK ({old_path})')
            
            if not dry_run and (center.logo or center.banner):
                center.save()
            
            self.stdout.write('')
        
        return fixed

    def fix_creator_fields(self, model_class, dry_run):
        """Fix CourseCreator profile picture paths."""
        fixed = 0
        
        for creator in model_class.objects.all():
            self.stdout.write(f'Creator: {creator.name}')
            
            if creator.profile_picture and creator.profile_picture.name:
                old_path = creator.profile_picture.name
                new_path = self.clean_path(old_path, 'profile_pictures/', prefix='course_creators/')
                
                if old_path != new_path:
                    self.stdout.write(f'  Profile: {old_path} -> {new_path}')
                    if not dry_run:
                        creator.profile_picture.name = new_path
                        creator.save()
                        fixed += 1
                else:
                    self.stdout.write(f'  Profile: OK ({old_path})')
            
            self.stdout.write('')
        
        return fixed

    def clean_path(self, path, upload_to_folder, prefix=''):
        """
        Clean up path by removing old prefixes and ensuring correct structure.
        
        Examples:
        - partner/logo.png -> logos/logo.png
        - logos/logo.png -> logos/logo.png (already correct)
        - center/logo.jpg -> logos/logo.jpg (with prefix='center/')
        """
        # Get just the filename
        filename = path.split('/')[-1]
        
        # If path already starts with the correct upload_to folder, keep it
        if path.startswith(upload_to_folder):
            return path
        
        # If path has prefix in it, remove it
        if prefix:
            path = path.replace(prefix, '')
        
        # Remove old 'partner/' or 'center/' or 'course_creators/' prefix
        path = path.replace('partner/', '')
        path = path.replace('center/', '')
        path = path.replace('course_creators/', '')
        
        # Get filename again after cleanup
        filename = path.split('/')[-1]
        
        # Return clean path
        return f'{upload_to_folder}{filename}'
