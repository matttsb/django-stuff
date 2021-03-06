# Generated by Django 3.0.4 on 2020-10-16 20:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=100)),
                ('slug', models.SlugField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('website', models.CharField(blank=True, max_length=100, null=True)),
                ('updated', models.DateField(blank=True, null=True)),
                ('visible', models.BooleanField(blank=True, default=False, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Parttypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mpn', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('dim', models.CharField(blank=True, max_length=100, null=True)),
                ('man', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='heating.Manufacturer')),
                ('parttype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='heating.Parttypes')),
            ],
            options={
                'ordering': ['mpn'],
            },
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=100, null=True, unique=True)),
                ('image', models.ImageField(null=True, upload_to='media/img')),
                ('keywords', models.CharField(max_length=200)),
                ('metad', models.CharField(blank=True, max_length=200, null=True)),
                ('intro', models.TextField(blank=True, null=True)),
                ('body', tinymce.models.HTMLField(blank=True, null=True)),
                ('posted', models.DateField(auto_now_add=True, db_index=True)),
                ('enable_comments', models.BooleanField()),
                ('publishdate', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('enddate', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('visible', models.BooleanField(blank=True, default=False, null=True)),
                ('promote', models.BooleanField(blank=True, default=False, null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='heating.BlogCategory')),
            ],
        ),
        migrations.CreateModel(
            name='Appliance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appid', models.CharField(blank=True, max_length=100, null=True)),
                ('nameandmodel', models.CharField(blank=True, max_length=100, null=True)),
                ('model', models.CharField(blank=True, max_length=100, null=True)),
                ('slug', models.CharField(blank=True, max_length=100)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('mpn', models.CharField(blank=True, max_length=100, null=True)),
                ('doclink', models.CharField(blank=True, max_length=200, null=True)),
                ('visible', models.BooleanField(default=False)),
                ('fuel', models.CharField(blank=True, choices=[('EL', 'ELECTRIC'), ('AS', 'AIR SOURCE'), ('GE', 'GEOTHERMAL'), ('LP', 'LPG'), ('LC', 'LPG Combi'), ('NG', 'Natural Gas'), ('NC', 'Natural Gas Combi'), ('CU', 'Combi'), ('OI', 'OIL')], max_length=2, null=True)),
                ('manufacturer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='heating.Manufacturer')),
                ('parts', models.ManyToManyField(blank=True, to='heating.Part')),
            ],
        ),
    ]
