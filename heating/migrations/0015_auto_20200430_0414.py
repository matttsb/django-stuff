# Generated by Django 3.0.4 on 2020-04-30 04:14

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('heating', '0014_auto_20200430_0405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='body',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
    ]
