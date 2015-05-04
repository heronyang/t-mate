# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tmate', '0005_auto_20150502_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='overview',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
