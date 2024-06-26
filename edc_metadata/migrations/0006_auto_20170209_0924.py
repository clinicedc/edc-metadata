# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-09 07:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("edc_metadata", "0005_auto_20170112_0602")]

    operations = [
        migrations.AlterField(
            model_name="crfmetadata",
            name="schedule_name",
            field=models.CharField(editable=False, max_length=25),
        ),
        migrations.AlterField(
            model_name="crfmetadata",
            name="visit_schedule_name",
            field=models.CharField(
                editable=False,
                help_text='the name of the visit schedule used to find the "schedule"',
                max_length=25,
            ),
        ),
        migrations.AlterField(
            model_name="requisitionmetadata",
            name="schedule_name",
            field=models.CharField(editable=False, max_length=25),
        ),
        migrations.AlterField(
            model_name="requisitionmetadata",
            name="visit_schedule_name",
            field=models.CharField(
                editable=False,
                help_text='the name of the visit schedule used to find the "schedule"',
                max_length=25,
            ),
        ),
    ]
