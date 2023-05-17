# Generated by Django 3.0.4 on 2020-05-12 21:23

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("edc_metadata", "0017_auto_20191024_1000"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="crfmetadata",
            options={
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("show_order",),
                "verbose_name": "Crf Metadata",
                "verbose_name_plural": "Crf Metadata",
            },
        ),
        migrations.AlterModelOptions(
            name="requisitionmetadata",
            options={
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("show_order",),
                "verbose_name": "Requisition Metadata",
                "verbose_name_plural": "Requisition Metadata",
            },
        ),
    ]
