# Generated by Django 4.2.7 on 2023-11-19 16:47

from django.db import migrations, models
import travel.models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0011_alter_trip_trip_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='trip_status',
            field=models.CharField(choices=[(travel.models.TripStatus['ACTIVE'], 'Active'), (travel.models.TripStatus['CANCELLED'], 'Cancelled'), (travel.models.TripStatus['COMPLETED'], 'Completed')], default='Active', max_length=20),
        ),
    ]
