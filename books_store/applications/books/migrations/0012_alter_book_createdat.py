# Generated by Django 4.2 on 2023-05-07 20:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0011_alter_book_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='createdAt',
            field=models.DateField(default=datetime.datetime(2023, 5, 7, 20, 18, 51, 9755, tzinfo=datetime.timezone.utc)),
        ),
    ]