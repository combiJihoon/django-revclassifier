# Generated by Django 2.2 on 2021-06-15 07:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CrawlResult',
        ),
        migrations.DeleteModel(
            name='UserInput',
        ),
    ]
