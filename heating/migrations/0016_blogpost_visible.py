# Generated by Django 3.0.4 on 2020-05-07 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heating', '0015_auto_20200430_0414'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='visible',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
