# Generated by Django 5.2.3 on 2025-07-03 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0007_rename_logourl_store_imageurl"),
    ]

    operations = [
        migrations.AlterField(
            model_name="store",
            name="imageUrl",
            field=models.ImageField(
                blank=True, null=True, upload_to="api/static/images/store_logos"
            ),
        ),
    ]
