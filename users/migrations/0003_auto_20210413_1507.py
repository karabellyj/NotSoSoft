# Generated by Django 3.1.7 on 2021-04-13 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('risk', '0003_remove_company_company_manager'),
        ('users', '0002_customuser_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='risk.company'),
        ),
    ]
