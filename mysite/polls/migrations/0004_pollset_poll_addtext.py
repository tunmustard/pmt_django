# Generated by Django 2.1.2 on 2018-11-02 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_pollset_require_authorization'),
    ]

    operations = [
        migrations.AddField(
            model_name='pollset',
            name='poll_addtext',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
