# Generated by Django 2.2.11 on 2020-03-22 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_book_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cost',
            field=models.IntegerField(default=500),
        ),
    ]
