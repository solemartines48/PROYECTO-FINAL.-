# Generated by Django 4.2.7 on 2023-11-11 22:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0002_passenger'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='passenger',
            name='user',
        ),
    ]
