# Generated by Django 5.0.4 on 2024-05-01 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serverpanel', '0015_server_start_command_server_stop_command'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='port',
            field=models.IntegerField(default=25565),
        ),
    ]