# Generated by Django 4.2.1 on 2023-12-19 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fooditems', to='menu.category'),
        ),
    ]
