# Generated by Django 2.1.2 on 2018-10-31 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='pub_date',
        ),
        migrations.AddField(
            model_name='pollset',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]