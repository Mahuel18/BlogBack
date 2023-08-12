# Generated by Django 4.2.3 on 2023-08-11 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_introduction'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='content',
            new_name='paragraph1',
        ),
        migrations.AddField(
            model_name='post',
            name='paragraph2',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='paragraph3',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='paragraph4',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='paragraph5',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
