# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-06 09:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_application_originlwritertyp'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='parent',
            field=models.IntegerField(default=0),
        ),
    ]
