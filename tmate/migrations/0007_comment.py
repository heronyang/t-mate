# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tmate', '0006_profile_overview'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('score', models.IntegerField(max_length=5, choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)])),
                ('author', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
