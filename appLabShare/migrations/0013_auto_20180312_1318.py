# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-12 13:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appLabShare', '0012_auto_20180312_1259'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='created_date',
            new_name='timePosted',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
