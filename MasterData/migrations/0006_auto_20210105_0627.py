# Generated by Django 3.1.4 on 2021-01-05 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MasterData', '0005_auto_20210105_0526'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ward',
            old_name='facility_id',
            new_name='facility',
        ),
    ]