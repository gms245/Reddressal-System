# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-07 17:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_userprofile_pos'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='activation_key',
            field=models.CharField(default='None', max_length=40),
            preserve_default=False,
        ),
    ]
