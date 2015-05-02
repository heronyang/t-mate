# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tmate', '0003_auto_20150427_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='website_url',
            field=models.URLField(max_length=256, blank=True),
            preserve_default=True,
        ),
    ]
