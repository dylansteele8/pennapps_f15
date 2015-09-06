from django.db import models
import soundcloud
import string
from pennapps_f15.settings.production import SOUNDCLOUD_CLIENT_ID

def playlist_default():
    return Playlist.objects.create().pk

class Song(models.Model):
    title = models.CharField(max_length=999)
    sid = models.CharField(max_length=999)
    genre = models.CharField(max_length=999)

    def __str__(self):
        return str(self.sid) + "-" + self.title

class PlaylistSong(models.Model):
    song = models.ForeignKey(Song)
    index = models.IntegerField()
    url = models.CharField(max_length=999, default="")

    def save(self, *args, **kwargs):
        if not self.pk:
            self.url = self.get_song_url()
        super(PlaylistSong, self).save(*args, **kwargs)

    def get_song_url(self):
        client = soundcloud.Client(client_id=SOUNDCLOUD_CLIENT_ID)
        track = client.get('/tracks/' + str(self.song.sid))
        stream_url = client.get(track.stream_url, allow_redirects=False)
        return stream_url.location
        

class Playlist(models.Model):
    songs = models.ManyToManyField(PlaylistSong, blank=True, null=True)
    current_song = models.IntegerField(default=0)

    def __str__(self):
        return self.pk + " " + self.current_song + " " + self.songs
        

class MyUser(models.Model):
    phone_number = models.IntegerField()
    joined_timestamp = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )
    liked_songs = models.ManyToManyField(Song, related_name="liked_songs")
    disliked_songs = models.ManyToManyField(Song, related_name="disliked_songs")
    playlist = models.ForeignKey(Playlist)

    def __str__(self):
        return str(self.phone_number)

    
