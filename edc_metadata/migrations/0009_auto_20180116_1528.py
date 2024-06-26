# Generated by Django 2.0.1 on 2018-01-16 13:28

import django.db.models.deletion
import edc_sites.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sites", "0002_alter_domain_unique"),
        ("edc_metadata", "0008_auto_20171211_2239"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="crfmetadata",
            managers=[("on_site", edc_sites.models.CurrentSiteManager())],
        ),
        migrations.AlterModelManagers(
            name="requisitionmetadata",
            managers=[("on_site", edc_sites.models.CurrentSiteManager())],
        ),
        migrations.AddField(
            model_name="crfmetadata",
            name="site",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="sites.Site",
            ),
        ),
        migrations.AddField(
            model_name="requisitionmetadata",
            name="site",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="sites.Site",
            ),
        ),
    ]
