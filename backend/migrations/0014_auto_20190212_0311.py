# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-12 03:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("backend", "0013_auto_20190209_0333")]

    operations = [
        migrations.AlterField(
            model_name="contact",
            name="contact_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="backend.ContactType"
            ),
        )
    ]
