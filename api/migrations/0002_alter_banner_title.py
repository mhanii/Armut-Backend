# Generated by Django 5.0 on 2024-01-03 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='title',
            field=models.CharField(default='', max_length=50, null=True),
        ),
    ]
