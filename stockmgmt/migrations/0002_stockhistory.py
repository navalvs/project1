# Generated by Django 5.0.3 on 2024-05-08 12:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stockmgmt", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="StockHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("item_name", models.CharField(blank=True, max_length=50, null=True)),
                ("quantity", models.IntegerField(blank=True, default="0", null=True)),
                (
                    "receive_quantity",
                    models.IntegerField(blank=True, default="0", null=True),
                ),
                ("receive_by", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "issue_quantity",
                    models.IntegerField(blank=True, default="0", null=True),
                ),
                ("issue_by", models.CharField(blank=True, max_length=50, null=True)),
                ("issue_to", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("created_by", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "reorder_level",
                    models.IntegerField(blank=True, default="0", null=True),
                ),
                ("last_update", models.DateTimeField(auto_now=True)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="stockmgmt.category",
                    ),
                ),
            ],
        ),
    ]