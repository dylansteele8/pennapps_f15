from django.db import models
from django.conf import settings
import soundcloud


class Song(models.Model):
    title = models.CharField(max_length=999)
    sid = models.CharField(max_length=999)
    genre = models.CharField(max_length=999)

    def __str__(self):
        return self.sid + "-" + self.title


class StationSong(models.Model):
    song = models.ForeignKey(Song)
    index = models.IntegerField()
    url = models.CharField(max_length=999, default="")

    def save(self, *args, **kwargs):
        if not self.pk:
            self.url = self.get_song_url()
        super(StationSong, self).save(*args, **kwargs)

    def get_song_url(self):
        client = soundcloud.Client(client_id=settings.SOUNDCLOUD_CLIENT_ID)
        track = client.get('/tracks/' + str(self.song.sid))
        stream_url = client.get(track.stream_url, allow_redirects=False)
        return stream_url.location

    def __str__(self):
        return self.song.title + " at " + str(self.index)


class Station(models.Model):
    songs = models.ManyToManyField(StationSong, blank=True, null=True)
    current_song = models.IntegerField(default=0)
    disliked_songs = models.ManyToManyField(Song, blank=True, null=True)
    created_timestamp = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )

    def __str__(self):
        return str(self.pk) + " " + str(self.current_song)


class Account(models.Model):
    phone_number = models.CharField(max_length=11)
    current_station = models.ForeignKey(Station, 
        related_name="current_station", 
        blank=True, null=True)
    stations = models.ManyToManyField(Station, 
        related_name="stations", 
        blank=True, null=True)
        