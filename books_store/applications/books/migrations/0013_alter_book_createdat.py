# Generated by Django 4.2 on 2023-05-07 20:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0012_alter_book_createdat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='createdAt',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]