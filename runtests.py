#!/usr/bin/env python
import django
import logging
import os
import sys

from django.conf import settings
from django.test.runner import DiscoverRunner
from edc_test_utils import DefaultTestSettings
from os.path import abspath, dirname

app_name = "edc_metadata"
base_dir = dirname(abspath(__file__))

DEFAULT_SETTINGS = DefaultTestSettings(
    calling_file=__file__,
    BASE_DIR=base_dir,
    APP_NAME=app_name,
    ETC_DIR=os.path.join(base_dir, app_name, "tests", "etc"),
    INSTALLED_APPS=[
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.contrib.sites",
        "django_crypto_fields.apps.AppConfig",
        "django_revision.apps.AppConfig",
        "rest_framework.authtoken",
        # "django_collect_offline.apps.AppConfig",
        # "django_collect_offline_files.apps.AppConfig",
        "multisite",
        "import_export",
        "edc_action_item.apps.AppConfig",
        "edc_appointment.apps.AppConfig",
        "edc_crf.apps.AppConfig",
        "edc_device.apps.AppConfig",
        "edc_identifier.apps.AppConfig",
        "edc_facility.apps.AppConfig",
        "edc_lab.apps.AppConfig",
        "edc_notification.apps.AppConfig",
        "edc_metadata_rules.apps.AppConfig",
        "edc_offstudy.apps.AppConfig",
        "edc_protocol.apps.AppConfig",
        "edc_reference.apps.AppConfig",
        "edc_registration.apps.AppConfig",
        "edc_sites.apps.AppConfig",
        "edc_timepoint.apps.AppConfig",
        "edc_visit_schedule.apps.AppConfig",
        "edc_visit_tracking.apps.AppConfig",
        "edc_metadata.apps.AppConfig",
    ],
    add_dashboard_middleware=True,
).settings


def main():
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)
    django.setup()
    tags = [t.split("=")[1] for t in sys.argv if t.startswith("--tag")]
    failures = DiscoverRunner(failfast=True, tags=tags).run_tests([f"{app_name}.tests"])
    sys.exit(failures)


if __name__ == "__main__":
    logging.basicConfig()
    main()
