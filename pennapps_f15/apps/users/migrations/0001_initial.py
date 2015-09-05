# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pennapps_f15.apps.users.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(default=b'G', max_length=2, choices=[(b'U', b'User'), (b'A', b'Admin')])),
                ('avatar', models.ImageField(default=b'', upload_to=pennapps_f15.apps.users.models.avatarUploadToFn, blank=True)),
                ('joined_timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
