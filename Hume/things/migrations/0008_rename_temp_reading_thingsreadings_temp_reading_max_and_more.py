# Generated by Django 5.1.2 on 2025-06-19 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('things', '0007_alter_things_localauthority_alter_things_location_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='thingsreadings',
            old_name='temp_reading',
            new_name='temp_reading_max',
        ),
        migrations.AddField(
            model_name='thingsreadings',
            name='temp_reading_min',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
