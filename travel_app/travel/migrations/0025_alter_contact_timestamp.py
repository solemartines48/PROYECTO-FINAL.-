# Generated by Django 4.2.7 on 2023-11-30 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0024_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]