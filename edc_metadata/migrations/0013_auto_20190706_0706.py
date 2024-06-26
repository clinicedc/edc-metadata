# Generated by Django 2.2.2 on 2019-07-06 05:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("edc_metadata", "0012_auto_20190627_2320")]

    operations = [
        migrations.RemoveIndex(
            model_name="crfmetadata", name="edc_metadat_subject_a76082_idx"
        ),
        migrations.RemoveIndex(
            model_name="requisitionmetadata", name="edc_metadat_subject_f96783_idx"
        ),
        migrations.AddField(
            model_name="crfmetadata",
            name="timepoint",
            field=models.DecimalField(decimal_places=1, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name="requisitionmetadata",
            name="timepoint",
            field=models.DecimalField(decimal_places=1, max_digits=6, null=True),
        ),
        migrations.AddIndex(
            model_name="crfmetadata",
            index=models.Index(
                fields=[
                    "subject_identifier",
                    "visit_schedule_name",
                    "schedule_name",
                    "visit_code",
                    "visit_code_sequence",
                    "timepoint",
                    "model",
                    "entry_status",
                    "show_order",
                ],
                name="edc_metadat_subject_1b2c7e_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="requisitionmetadata",
            index=models.Index(
                fields=[
                    "subject_identifier",
                    "visit_schedule_name",
                    "schedule_name",
                    "visit_code",
                    "visit_code_sequence",
                    "timepoint",
                    "model",
                    "entry_status",
                    "show_order",
                    "panel_name",
                ],
                name="edc_metadat_subject_fb1a00_idx",
            ),
        ),
    ]
