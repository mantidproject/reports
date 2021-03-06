# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-25 18:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=32, unique=True)),
                ('city', models.CharField(max_length=32)),
                ('region', models.CharField(max_length=32)),
                ('country', models.CharField(max_length=32)),
                ('latitude', models.CharField(max_length=32)),
                ('longitude', models.CharField(max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='usage',
            name='ip',
            field=models.CharField(blank=True, default=b'', max_length=32),
        ),
    ]
