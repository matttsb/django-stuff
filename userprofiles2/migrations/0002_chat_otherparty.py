# Generated by Django 3.0.4 on 2020-04-22 05:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userprofiles2', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='otherparty',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='otherparty', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
