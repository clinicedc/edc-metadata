# Generated by Django 2.2.2 on 2019-09-22 02:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("edc_metadata", "0015_auto_20190709_0009")]

    operations = [
        migrations.AlterField(
            model_name="crfmetadata",
            name="subject_identifier",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="requisitionmetadata",
            name="subject_identifier",
            field=models.CharField(max_length=50),
        ),
    ]
