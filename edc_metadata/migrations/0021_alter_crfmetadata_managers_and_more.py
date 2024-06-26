# Generated by Django 4.2.1 on 2023-07-07 19:32

import edc_sites.models
from django.db import migrations

import edc_metadata.managers


class Migration(migrations.Migration):
    dependencies = [
        ("edc_metadata", "0020_alter_crfmetadata_options_and_more"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="crfmetadata",
            managers=[
                ("objects", edc_metadata.managers.CrfMetadataManager()),
                ("on_site", edc_sites.models.CurrentSiteManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name="requisitionmetadata",
            managers=[
                ("objects", edc_metadata.managers.RequisitionMetadataManager()),
                ("on_site", edc_sites.models.CurrentSiteManager()),
            ],
        ),
    ]
