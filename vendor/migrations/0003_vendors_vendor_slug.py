# Generated by Django 4.2.1 on 2023-12-16 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0002_alter_vendors_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendors',
            name='vendor_slug',
            field=models.SlugField(blank=True, max_length=100),
        ),
    ]
