# Generated migration for separate S3 bucket storage

from django.db import migrations, models
import course_partnerships.storage


class Migration(migrations.Migration):

    dependencies = [
        ('course_partnerships', '0008_alter_center_name_alter_center_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='center',
            name='banner',
            field=models.ImageField(blank=True, help_text='Upload only image file with .png, .jpeg, .jpg extension.', null=True, storage=course_partnerships.storage.CenterLogoStorage(), upload_to='banners/', validators=[course_partnerships.validators.validate_bannner_extension], verbose_name='Banner'),
        ),
        migrations.AlterField(
            model_name='center',
            name='logo',
            field=models.ImageField(help_text='Upload only image file with .png, .jpeg, .jpg extension. Recommended image size: W 240px * H 340px', storage=course_partnerships.storage.CenterLogoStorage(), upload_to='logos/', validators=[course_partnerships.validators.validate_bannner_extension], verbose_name='logo'),
        ),
        migrations.AlterField(
            model_name='coursecreator',
            name='profile_picture',
            field=models.ImageField(blank=True, help_text='Upload only image file with .png, .jpeg, .jpg extension.', null=True, storage=course_partnerships.storage.CourseCreatorStorage(), upload_to='profile_pictures/', validators=[course_partnerships.validators.validate_bannner_extension], verbose_name='Profile Picture'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='banner',
            field=models.ImageField(blank=True, help_text='Upload only image file with .png, .jpeg, .jpg extension.', null=True, storage=course_partnerships.storage.PartnerLogoStorage(), upload_to='banners/', validators=[course_partnerships.validators.validate_bannner_extension], verbose_name='Banner'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='logo',
            field=models.ImageField(help_text='Upload only image file with .png, .jpeg, .jpg extension. Recommended image size: W 240px * H 340px', storage=course_partnerships.storage.PartnerLogoStorage(), upload_to='logos/', validators=[course_partnerships.validators.validate_bannner_extension], verbose_name='logo'),
        ),
    ]
