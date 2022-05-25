# Generated by Django 4.0.4 on 2022-05-25 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("edc_metadata", "0018_auto_20200513_0023"),
    ]

    operations = [
        migrations.AlterField(
            model_name="crfmetadata",
            name="entry_status",
            field=models.CharField(
                choices=[
                    ("REQUIRED", "New"),
                    ("KEYED", "Keyed"),
                    ("missed", "Missed"),
                    ("NOT_REQUIRED", "Not required"),
                ],
                db_index=True,
                default="REQUIRED",
                max_length=25,
            ),
        ),
        migrations.AlterField(
            model_name="requisitionmetadata",
            name="entry_status",
            field=models.CharField(
                choices=[
                    ("REQUIRED", "New"),
                    ("KEYED", "Keyed"),
                    ("missed", "Missed"),
                    ("NOT_REQUIRED", "Not required"),
                ],
                db_index=True,
                default="REQUIRED",
                max_length=25,
            ),
        ),
    ]
