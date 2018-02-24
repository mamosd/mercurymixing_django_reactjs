# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mixing.permissions
import private_storage.fields
import private_storage.storage


class Migration(migrations.Migration):

    dependencies = [
        ('mixing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='attachment',
            field=private_storage.fields.PrivateFileField(storage=private_storage.storage.PrivateStorage(), upload_to=mixing.permissions.private_comment_path, max_length=255, verbose_name='Attachment', blank=True),
        ),
        migrations.AlterField(
            model_name='finalfile',
            name='attachment',
            field=private_storage.fields.PrivateFileField(storage=private_storage.storage.PrivateStorage(), upload_to=mixing.permissions.private_final_path, max_length=255, verbose_name='Attachment'),
        ),
        migrations.AlterField(
            model_name='track',
            name='file',
            field=private_storage.fields.PrivateFileField(storage=private_storage.storage.PrivateStorage(), upload_to=mixing.permissions.private_track_path, max_length=255, verbose_name='File'),
        ),
    ]
