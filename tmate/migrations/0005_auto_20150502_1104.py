# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tmate', '0004_profile_website_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='website_url',
            new_name='website',
        ),
    ]
