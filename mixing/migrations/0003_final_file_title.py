# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mixing', '0002_private_files'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='finalfile',
            name='notes',
        ),
        migrations.AddField(
            model_name='finalfile',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Title', blank=True),
        ),
    ]
