# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-27 03:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_comment_html_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_id', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('video_description', models.TextField()),
                ('thumbnail', models.ImageField(blank=True, upload_to='youtude-%y%m%d')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]