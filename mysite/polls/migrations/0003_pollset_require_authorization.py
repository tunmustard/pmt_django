# Generated by Django 2.1.2 on 2018-10-31 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20181031_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='pollset',
            name='require_authorization',
            field=models.BooleanField(default=True),
        ),
    ]
