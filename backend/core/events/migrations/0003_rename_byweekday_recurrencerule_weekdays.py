# Generated by Django 5.0.6 on 2025-06-08 00:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_rename_until_recurrencerule_end_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recurrencerule',
            old_name='byweekday',
            new_name='weekdays',
        ),
    ]
