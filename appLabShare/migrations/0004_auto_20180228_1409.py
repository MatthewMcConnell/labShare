# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-28 14:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appLabShare', '0003_auto_20180228_1229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='courses',
        ),
        migrations.RemoveField(
            model_name='student',
            name='friends',
        ),
        migrations.RemoveField(
            model_name='student',
            name='labs',
        ),
        migrations.RemoveField(
            model_name='student',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='tutor',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='lab',
            name='tutors',
        ),
        migrations.AddField(
            model_name='lab',
            name='peopleInLab',
            field=models.ManyToManyField(to='appLabShare.UserProfile'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='courses',
            field=models.ManyToManyField(to='appLabShare.Course'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='friends',
            field=models.ManyToManyField(to='appLabShare.UserProfile'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='isStudent',
            field=models.BooleanField(default=True),
        ),
        migrations.DeleteModel(
            name='Student',
        ),
        migrations.DeleteModel(
            name='Tutor',
        ),
    ]