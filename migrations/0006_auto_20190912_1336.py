# Generated by Django 2.2.5 on 2019-09-12 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20190417_1630'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='terrauser',
            options={'ordering': ['id'], 'permissions': (('can_manage_users', 'Is able to create, delete, update users'), ('can_manage_groups', 'Is able to create, delete, update groups'))},
        ),
    ]
