# Generated by Django 3.1.3 on 2020-11-17 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terra_accounts', '0008_auto_20191025_1041'),
    ]

    operations = [
        migrations.AddField(
            model_name='terrapermission',
            name='module',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]