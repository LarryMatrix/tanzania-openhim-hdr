# Generated by Django 3.1.4 on 2021-01-12 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MasterData', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ICD10Mapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icd10_code', models.CharField(max_length=255)),
                ('icd10_name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'icd10_mapping',
            },
        ),
    ]