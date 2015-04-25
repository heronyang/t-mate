# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HashTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('content', models.CharField(max_length=1024)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_type', models.IntegerField(default=0, choices=[(0, b'programmer'), (1, b'designer'), (2, b'individual hunter'), (3, b'company hunter')])),
                ('picture_url', models.CharField(max_length=256, blank=True)),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('resume_url', models.CharField(max_length=256, blank=True)),
                ('portfolio', models.CharField(max_length=256, blank=True)),
                ('github_url', models.CharField(max_length=256, blank=True)),
                ('position', models.CharField(max_length=1024, blank=True)),
                ('skill', models.ManyToManyField(related_name='hashtag', to='tmate.HashTag')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
