# Generated by Django 5.0.4 on 2024-04-28 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('serverpanel', '0007_remove_server_configuration_server_configuration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='path',
        ),
    ]
