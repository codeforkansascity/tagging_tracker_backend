# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-09 03:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("backend", "0012_auto_20190209_0332")]

    operations = [
        migrations.AlterField(
            model_name="contact", name="phone", field=models.CharField(max_length=25)
        )
    ]
