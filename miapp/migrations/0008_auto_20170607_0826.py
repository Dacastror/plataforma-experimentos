# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-07 08:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miapp', '0007_auto_20170607_0824'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Author',
            new_name='Tema',
        ),
    ]