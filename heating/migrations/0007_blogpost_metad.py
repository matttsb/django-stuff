# Generated by Django 3.0.4 on 2020-04-10 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heating', '0006_auto_20200410_0127'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='metad',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
