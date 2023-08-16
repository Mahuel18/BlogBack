# Generated by Django 4.2.3 on 2023-08-15 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_users_email_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='Email_Address',
        ),
        migrations.AddField(
            model_name='users',
            name='email',
            field=models.EmailField(blank=True, default=None, max_length=60, null=True, unique=True, verbose_name='email'),
        ),
    ]