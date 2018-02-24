# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, editable=False)),
                ('updated', models.DateTimeField(null=True, editable=False)),
                ('content', models.TextField(verbose_name='Content')),
                ('attachment', models.FileField(upload_to='comments', max_length=255, verbose_name='Attachment', blank=True)),
                ('author', models.ForeignKey(related_name='comments', verbose_name='Author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created'],
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
            },
        ),
        migrations.CreateModel(
            name='FinalFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, editable=False)),
                ('updated', models.DateTimeField(null=True, editable=False)),
                ('notes', models.TextField(verbose_name='Notes', blank=True)),
                ('attachment', models.FileField(upload_to='finals', max_length=255, verbose_name='Attachment')),
            ],
            options={
                'verbose_name': 'final file',
                'verbose_name_plural': 'final files',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
            ],
            options={
                'verbose_name': 'group',
                'verbose_name_plural': 'groups',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, editable=False)),
                ('updated', models.DateTimeField(null=True, editable=False)),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('active', models.BooleanField(default=True, verbose_name='Active', help_text='Indicates if users can upload files')),
                ('status', models.PositiveIntegerField(default=1, verbose_name='Status', choices=[(1, 'Waiting for files'), (2, 'In progress'), (3, 'Mixing complete'), (4, 'Waiting for revision files'), (5, 'Revision in progress'), (6, 'Revision complete')])),
                ('priority', models.SmallIntegerField(default=10, help_text='Lower numbers indicate a higher priority for this project', verbose_name='Priority', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('owner', models.ForeignKey(related_name='projects', verbose_name='Owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'project',
                'verbose_name_plural': 'projects',
            },
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('project', models.ForeignKey(related_name='songs', to='mixing.Project')),
            ],
            options={
                'verbose_name': 'song',
                'verbose_name_plural': 'songs',
            },
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to='tracks', max_length=255, verbose_name='File')),
                ('group', models.ForeignKey(related_name='tracks', to='mixing.Group')),
            ],
            options={
                'verbose_name': 'track',
                'verbose_name_plural': 'tracks',
            },
        ),
        migrations.AddField(
            model_name='group',
            name='song',
            field=models.ForeignKey(related_name='groups', to='mixing.Song'),
        ),
        migrations.AddField(
            model_name='finalfile',
            name='project',
            field=models.ForeignKey(related_name='final_files', to='mixing.Project'),
        ),
        migrations.AddField(
            model_name='comment',
            name='project',
            field=models.ForeignKey(related_name='comments', to='mixing.Project'),
        ),
    ]
