# Generated by Django 5.1.2 on 2024-10-16 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, unique=True),
        ),
    ]
