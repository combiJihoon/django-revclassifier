# Generated by Django 2.2 on 2021-05-30 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='position',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]