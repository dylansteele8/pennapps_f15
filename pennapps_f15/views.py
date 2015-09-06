from django.shortcuts import render
import twilio.twiml
from django_twilio.decorators import twilio_view
import soundcloud
import requests
import urllib
import json
import random
from apps.users.models import *
from pennapps_f15.settings.production import SOUNDCLOUD_CLIENT_ID

GENRES = ["Jazz", 
          "Hip Hop", "Blues", "Indie Pop", 
          "Country", "Reggae", "Pop", 
          "Classical", "Bluegrass", "RB"]

def previous_track(user):
    user.playlist.current_song -= 2
    user.playlist.save()
    return play_station(user.playlist.pk)


def next_track(user):
    return play_station(user.playlist.pk)


def dislike(user):
    playlist_song = user.playlist.songs.get(index=user.playlist.current_song-1)
    user.disliked_songs.add(playlist_song.song)
    user.save()
    return play_station(user.playlist.pk)


def save(user):
    resp = twilio.twiml.Response()
    resp.say("Enter %04d # next time to start where you left off or share with \
              your friends" % (user.playlist.pk))
    return resp

ACTIONS = {
            0: save, 
            1: dislike, 2: None, 3: None, 
            4: previous_track, 5: None, 6: next_track,
            7: None, 8: None, 9: None 
          }

# Create your views here.
@twilio_view
def home(request):
    # Get the caller's phone number from the incoming Twilio request
    from_number = int(request.POST.get('From', None))
    if from_number:
        try:
            MyUser.objects.get(phone_number=from_number)
        except:
            MyUser.objects.create(phone_number=from_number, 
                                  playlist=Playlist.objects.create())

    return menu()


def menu():
    resp = twilio.twiml.Response()
    with resp.gather(action="/play") as g:
        g.say("Welcome to Phonograph")
        g.pause(length=1)
        for i in xrange(len(GENRES)):
            g.say("For " + GENRES[i] + ", press " + str(i))
        g.say("Or enter your station code and press pound")
    return resp


@twilio_view
def play(request):    
    from_number = request.POST.get('From', None)
    user = MyUser.objects.get(phone_number=from_number)
    if request.method == 'POST':
        n = request.POST.get('Digits', 1)
        if len(n) == 1:
            genre = GENRES[int(n)]
            pid = create_station(user, genre)
        elif len(n) == 4:
            pid = int(n)
    return play_station(pid)


def create_station(user, genre): 
    artists = get_artists(genre)
    artists = artists['artists']['items']
    client = soundcloud.Client(client_id=SOUNDCLOUD_CLIENT_ID)
    for artist in artists:
        tracks = client.get('/tracks', q=artist['name'], streamable=True)
        for track in tracks:
            if track.streamable:
                song = Song.objects.create(title=track.title, sid=track.id, genre=track.genre)
                playlist_song = PlaylistSong.objects.create(song=song, 
                    index=user.playlist.songs.count())
                user.playlist.songs.add(playlist_song)
                break
    return user.playlist.pk

def play_station(pid):
    resp = twilio.twiml.Response()
    # for p in Playlist.objects.all():
        # print(p.pk, p.current_song)
    playlist = Playlist.objects.get(pk=pid)
    song = playlist.songs.get(index=playlist.current_song)
    with resp.gather(action="/controls", numDigits=1) as g:
        g.say("Playing " + song.song.title)
        g.play(song.url)
        playlist.current_song += 1
        playlist.save()
    resp.redirect(url="/controls", method="GET")

    return resp

@twilio_view
def controls(request):
    num = 0
    
    if request.method == 'POST':
        from_number = request.POST.get('From', None)
        user = MyUser.objects.get(phone_number=from_number)
        num = int(request.POST.get('Digits', 0))
    elif request.method == 'GET':
        from_number = request.GET.get('From', None)
        user = MyUser.objects.get(phone_number=from_number)
        num = 6

    return ACTIONS[num](user)


def get_artists(genre):
    url = "https://api.spotify.com/v1/search?q=* genre:\"" + genre + "\"&type=artist&limit=10"
    headers = { "User-Agent": "Mozilla/5.0" }
    response = requests.get(url, headers=headers)
    return json.loads(response.content)


def get_top_songs(artist):
    url = "https://api.spotify.com/v1/artists/" + artist + "/top-tracks?country=US"
    headers = { "User-Agent": "Mozilla/5.0" }
    response = requests.get(url, headers=headers)
    return json.loads(response.content)
