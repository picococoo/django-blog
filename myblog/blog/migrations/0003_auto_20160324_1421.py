# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-24 14:21
from __future__ import unicode_literals

from django.db import migrations
import django_markdown.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20160321_0152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='body',
            field=django_markdown.models.MarkdownField(),
        ),
    ]
