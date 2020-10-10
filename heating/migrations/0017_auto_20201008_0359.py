# Generated by Django 3.0.4 on 2020-10-08 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heating', '0016_blogpost_visible'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='image',
            field=models.ImageField(null=True, upload_to='media/img'),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='promote',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
