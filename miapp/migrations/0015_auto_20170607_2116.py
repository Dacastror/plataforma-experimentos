# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-07 21:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miapp', '0014_auto_20170607_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revision',
            name='tiempo',
            field=models.TimeField(null=True),
        ),
    ]
