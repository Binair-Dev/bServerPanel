# Generated by Django 5.0.4 on 2024-04-26 09:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serverpanel', '0002_game_rank_user_rank_server_command_transaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='rank',
        ),
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='serverpanel.rank'),
        ),
    ]
