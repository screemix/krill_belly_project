# Generated by Django 2.2.11 on 2020-03-22 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='_id',
        ),
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
