# Generated by Django 4.2.7 on 2023-11-28 01:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("edc_metadata", "0023_alter_crfmetadata_device_created_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="crfmetadata",
            old_name="current_entry_title",
            new_name="model_verbose_name",
        ),
        migrations.RenameField(
            model_name="requisitionmetadata",
            old_name="current_entry_title",
            new_name="model_verbose_name",
        ),
    ]
