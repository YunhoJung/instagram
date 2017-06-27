# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-26 21:14
from __future__ import unicode_literals

from django.db import migrations, models
import utils.fields.custom_imagefield


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0006_user_img_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('d', 'Django'), ('f', 'Facebook')], default='d', max_length=1),
        ),
        migrations.AlterField(
            model_name='user',
            name='img_profile',
            field=utils.fields.custom_imagefield.CustomImageField(blank=True, upload_to='member-%y%m%d'),
        ),
    ]