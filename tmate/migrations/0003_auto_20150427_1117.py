# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tmate', '0002_profile_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='skill',
        ),
        migrations.AddField(
            model_name='profile',
            name='skills',
            field=models.ManyToManyField(related_name='hashtag', to='tmate.HashTag'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='github_url',
            field=models.URLField(max_length=256, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='portfolio',
            field=models.URLField(max_length=256, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='resume_url',
            field=models.URLField(max_length=256, blank=True),
            preserve_default=True,
        ),
    ]
