# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-04 13:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_application_reciever'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='isprocessed',
            field=models.BooleanField(default=False),
        ),
    ]
