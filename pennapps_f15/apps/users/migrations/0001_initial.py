# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_number', models.CharField(max_length=11)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=999)),
                ('sid', models.CharField(max_length=999)),
                ('genre', models.CharField(max_length=999)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('current_song', models.IntegerField(default=0)),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('disliked_songs', models.ManyToManyField(to='users.Song', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StationSong',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index', models.IntegerField()),
                ('url', models.CharField(default=b'', max_length=999)),
                ('song', models.ForeignKey(to='users.Song')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='station',
            name='songs',
            field=models.ManyToManyField(to='users.StationSong', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='current_station',
            field=models.ForeignKey(related_name='current_station', blank=True, to='users.Station', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='stations',
            field=models.ManyToManyField(related_name='stations', null=True, to='users.Station', blank=True),
            preserve_default=True,
        ),
    ]
