# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-25 07:55
from __future__ import unicode_literals

import django_audit_fields.fields.uuid_auto_field
import django_extensions.db.fields
import django_revision.revision_field
import edc_model_fields.fields.hostname_modification_field
import edc_model_fields.fields.userfield
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CrfMetadata",
            fields=[
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                (
                    "user_created",
                    edc_model_fields.fields.userfield.UserField(
                        blank=True,
                        editable=False,
                        max_length=50,
                        verbose_name="user created",
                    ),
                ),
                (
                    "user_modified",
                    edc_model_fields.fields.userfield.UserField(
                        blank=True,
                        editable=False,
                        max_length=50,
                        verbose_name="user modified",
                    ),
                ),
                (
                    "hostname_created",
                    models.CharField(
                        default="mac2-2.local",
                        editable=False,
                        help_text="System field. (modified on create only)",
                        max_length=50,
                    ),
                ),
                (
                    "hostname_modified",
                    edc_model_fields.fields.hostname_modification_field.HostnameModificationField(
                        blank=True,
                        editable=False,
                        help_text="System field. (modified on every save)",
                        max_length=50,
                    ),
                ),
                (
                    "revision",
                    django_revision.revision_field.RevisionField(
                        blank=True,
                        editable=False,
                        help_text="System field. Git repository tag:branch:commit.",
                        max_length=75,
                        null=True,
                        verbose_name="Revision",
                    ),
                ),
                (
                    "id",
                    django_audit_fields.fields.uuid_auto_field.UUIDAutoField(
                        blank=True,
                        editable=False,
                        help_text="System auto field. UUID primary key.",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "subject_identifier",
                    models.CharField(
                        editable=False, max_length=50, verbose_name="Subject Identifier"
                    ),
                ),
                ("visit_schedule_name", models.CharField(max_length=25)),
                ("schedule_name", models.CharField(max_length=25)),
                ("visit_code", models.CharField(max_length=25)),
                ("model", models.CharField(max_length=50)),
                ("current_entry_title", models.CharField(max_length=250, null=True)),
                ("show_order", models.IntegerField()),
                (
                    "entry_status",
                    models.CharField(
                        choices=[
                            ("REQUIRED", "New"),
                            ("KEYED", "Keyed"),
                            ("MISSED", "Missed"),
                            ("NOT_REQUIRED", "Not required"),
                        ],
                        db_index=True,
                        default="REQUIRED",
                        max_length=25,
                    ),
                ),
                ("due_datetime", models.DateTimeField(blank=True, null=True)),
                ("report_datetime", models.DateTimeField(blank=True, null=True)),
                (
                    "entry_comment",
                    models.TextField(blank=True, max_length=250, null=True),
                ),
                ("close_datetime", models.DateTimeField(blank=True, null=True)),
                ("fill_datetime", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "verbose_name": "Crf Metadata",
                "verbose_name_plural": "Crf Metadata",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="RequisitionMetadata",
            fields=[
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                (
                    "user_created",
                    edc_model_fields.fields.userfield.UserField(
                        blank=True,
                        editable=False,
                        max_length=50,
                        verbose_name="user created",
                    ),
                ),
                (
                    "user_modified",
                    edc_model_fields.fields.userfield.UserField(
                        blank=True,
                        editable=False,
                        max_length=50,
                        verbose_name="user modified",
                    ),
                ),
                (
                    "hostname_created",
                    models.CharField(
                        default="mac2-2.local",
                        editable=False,
                        help_text="System field. (modified on create only)",
                        max_length=50,
                    ),
                ),
                (
                    "hostname_modified",
                    edc_model_fields.fields.hostname_modification_field.HostnameModificationField(
                        blank=True,
                        editable=False,
                        help_text="System field. (modified on every save)",
                        max_length=50,
                    ),
                ),
                (
                    "revision",
                    django_revision.revision_field.RevisionField(
                        blank=True,
                        editable=False,
                        help_text="System field. Git repository tag:branch:commit.",
                        max_length=75,
                        null=True,
                        verbose_name="Revision",
                    ),
                ),
                (
                    "id",
                    django_audit_fields.fields.uuid_auto_field.UUIDAutoField(
                        blank=True,
                        editable=False,
                        help_text="System auto field. UUID primary key.",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "subject_identifier",
                    models.CharField(
                        editable=False, max_length=50, verbose_name="Subject Identifier"
                    ),
                ),
                ("visit_schedule_name", models.CharField(max_length=25)),
                ("schedule_name", models.CharField(max_length=25)),
                ("visit_code", models.CharField(max_length=25)),
                ("model", models.CharField(max_length=50)),
                ("current_entry_title", models.CharField(max_length=250, null=True)),
                ("show_order", models.IntegerField()),
                (
                    "entry_status",
                    models.CharField(
                        choices=[
                            ("REQUIRED", "New"),
                            ("KEYED", "Keyed"),
                            ("MISSED", "Missed"),
                            ("NOT_REQUIRED", "Not required"),
                        ],
                        db_index=True,
                        default="REQUIRED",
                        max_length=25,
                    ),
                ),
                ("due_datetime", models.DateTimeField(blank=True, null=True)),
                ("report_datetime", models.DateTimeField(blank=True, null=True)),
                (
                    "entry_comment",
                    models.TextField(blank=True, max_length=250, null=True),
                ),
                ("close_datetime", models.DateTimeField(blank=True, null=True)),
                ("fill_datetime", models.DateTimeField(blank=True, null=True)),
                ("panel_name", models.CharField(max_length=50, null=True)),
            ],
            options={
                "verbose_name": "Requisition Metadata",
                "verbose_name_plural": "Requisition Metadata",
                "abstract": False,
            },
        ),
        migrations.AlterUniqueTogether(
            name="requisitionmetadata",
            unique_together=set(
                [
                    (
                        "subject_identifier",
                        "visit_schedule_name",
                        "schedule_name",
                        "visit_code",
                        "model",
                        "panel_name",
                    )
                ]
            ),
        ),
        migrations.AlterUniqueTogether(
            name="crfmetadata",
            unique_together=set(
                [
                    (
                        "subject_identifier",
                        "visit_schedule_name",
                        "schedule_name",
                        "visit_code",
                        "model",
                    )
                ]
            ),
        ),
    ]
