# Generated by Django 2.0 on 2018-01-14 19:17

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poim',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326),
        ),
    ]
