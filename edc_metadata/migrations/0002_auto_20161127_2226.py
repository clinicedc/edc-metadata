# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-27 22:26
from __future__ import unicode_literals

import edc_utils
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("edc_metadata", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="crfmetadata",
            name="created",
            field=models.DateTimeField(default=edc_utils.date.get_utcnow, editable=False),
        ),
        migrations.AlterField(
            model_name="crfmetadata",
            name="modified",
            field=models.DateTimeField(default=edc_utils.date.get_utcnow, editable=False),
        ),
        migrations.AlterField(
            model_name="requisitionmetadata",
            name="created",
            field=models.DateTimeField(default=edc_utils.date.get_utcnow, editable=False),
        ),
        migrations.AlterField(
            model_name="requisitionmetadata",
            name="modified",
            field=models.DateTimeField(default=edc_utils.date.get_utcnow, editable=False),
        ),
    ]
