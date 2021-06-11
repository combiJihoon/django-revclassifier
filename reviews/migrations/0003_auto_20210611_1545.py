# Generated by Django 2.2 on 2021-06-11 06:45

from django.db import migrations, models
import reviews.validators


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20210610_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='r_kakao',
            field=models.CharField(default='', max_length=20, validators=[reviews.validators.validate_symbols]),
        ),
    ]
