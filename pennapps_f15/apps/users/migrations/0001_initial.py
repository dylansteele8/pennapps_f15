# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_number', models.IntegerField()),
                ('joined_timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('current_song', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlaylistSong',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index', models.IntegerField()),
                ('url', models.CharField(default=b'', max_length=999)),
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
        migrations.AddField(
            model_name='playlistsong',
            name='song',
            field=models.ForeignKey(to='users.Song'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='playlist',
            name='songs',
            field=models.ManyToManyField(to='users.PlaylistSong', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='myuser',
            name='disliked_songs',
            field=models.ManyToManyField(related_name='disliked_songs', to='users.Song'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='myuser',
            name='liked_songs',
            field=models.ManyToManyField(related_name='liked_songs', to='users.Song'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='myuser',
            name='playlist',
            field=models.ForeignKey(to='users.Playlist'),
            preserve_default=True,
        ),
    ]
