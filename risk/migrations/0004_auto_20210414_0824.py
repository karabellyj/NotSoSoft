# Generated by Django 3.1.7 on 2021-04-14 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('risk', '0003_remove_company_company_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='estimated_end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='real_end',
            field=models.DateField(blank=True, null=True),
        ),
    ]
