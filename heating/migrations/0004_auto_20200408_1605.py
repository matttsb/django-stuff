# Generated by Django 3.0.4 on 2020-04-08 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('heating', '0003_auto_20200408_0122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appliance',
            name='manufacturer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='heating.Manufacturer'),
        ),
    ]
