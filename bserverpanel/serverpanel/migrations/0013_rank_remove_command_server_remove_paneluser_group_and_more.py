# Generated by Django 5.0.4 on 2024-04-26 12:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serverpanel', '0012_paneluser_alter_server_user_alter_transaction_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='command',
            name='server',
        ),
        migrations.RemoveField(
            model_name='paneluser',
            name='group',
        ),
        migrations.RemoveField(
            model_name='paneluser',
            name='user',
        ),
        migrations.RemoveField(
            model_name='server',
            name='user',
        ),
        migrations.AddField(
            model_name='paneluser',
            name='email',
            field=models.EmailField(default=None, max_length=255, unique=True),
        ),
        migrations.AddField(
            model_name='paneluser',
            name='server_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='paneluser',
            name='username',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AddField(
            model_name='server',
            name='owner',
            field=models.ManyToManyField(to='serverpanel.paneluser'),
        ),
        migrations.RemoveField(
            model_name='server',
            name='configuration',
        ),
        migrations.AlterField(
            model_name='server',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serverpanel.game'),
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='user',
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
                ('commands', models.ManyToManyField(to='serverpanel.command')),
            ],
        ),
        migrations.AddField(
            model_name='paneluser',
            name='rank',
            field=models.ManyToManyField(to='serverpanel.rank'),
        ),
        migrations.AddField(
            model_name='server',
            name='configuration',
            field=models.ManyToManyField(to='serverpanel.configuration'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='user',
            field=models.ManyToManyField(to='serverpanel.paneluser'),
        ),
    ]
