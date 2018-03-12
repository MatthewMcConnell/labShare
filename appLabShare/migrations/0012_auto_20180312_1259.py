# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-12 12:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('appLabShare', '0011_auto_20180312_1248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='timePosted',
        ),
        migrations.AddField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]