# Generated by Django 5.0.4 on 2024-05-01 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('serverpanel', '0026_remove_port_server_port_server'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='port',
            name='server',
        ),
    ]
