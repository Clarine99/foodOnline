# Generated by Django 4.2.1 on 2023-11-17 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.RenameField(
            model_name='fooditem',
            old_name='product',
            new_name='vendor',
        ),
    ]
