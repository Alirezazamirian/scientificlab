# Generated by Django 5.0.6 on 2024-12-20 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0007_alter_lastarticle_score"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="subheadarticle",
            name="is_free",
        ),
        migrations.AddField(
            model_name="lastarticle",
            name="is_free",
            field=models.BooleanField(default=False, verbose_name="Is Free"),
        ),
    ]
