import twilio.twiml
import soundcloud
import requests,urllib,json
from unidecode import unidecode
from apps.users.models import *
from django.conf import settings
from django_twilio.decorators import twilio_view
from django.shortcuts import render, redirect

MAX_DURATION = 300000 #in ms 
GENRES = ["Jazz", 
          "Hip Hop", "Blues", "Indie Pop", 
          "Country", "Reggae", "Pop", 
          "Classical", "Bluegrass", "RB"]


@twilio_view
def home(request):
    resp = twilio.twiml.Response()
    with resp.gather(action="/play") as g:
        g.say("Welcome to Phonograph")
        g.pause(length=1)
        for i in xrange(len(GENRES)):
            g.say("For " + GENRES[i] + ", press " + str(i))
        g.say("Or enter your station code and press pound")
    resp.pause(length=3)
    return resp


@twilio_view
def play(request):    
    if request.method == 'POST':
        resp = twilio.twiml.Response()
        n = request.POST.get('Digits', None)
        phone_number = request.POST.get('From', None)
        if len(n) == 1:
            genre = GENRES[int(n)]
            resp.say("Starting new " + genre + " station")
            station_id = create_station(genre, phone_number)
        elif len(n) == 4:
            resp.say("Resuming station " + n)
            station_id = int(n)
        else:
            resp.say("Please enter a valid genre or station ID")
            return redirect('home')
    return play_station(station_id)


def create_station(genre, phone_number):
    station = Station.objects.create()
    account, created = Account.objects.get_or_create(phone_number=phone_number)
    account.stations.add(station)
    account.current_station = station
    account.save()
    artists = get_artists(genre)
    client = soundcloud.Client(client_id=settings.SOUNDCLOUD_CLIENT_ID)
    for artist in artists:
        tracks = client.get('/tracks', q=artist['name'], streamable=True)
        for track in tracks:
            if track.stream_url and track.streamable and track.duration < MAX_DURATION:
                try:
                    song = Song.objects.create(
                        title=unidecode(track.title),
                        sid=track.id, 
                        genre=unidecode(track.genre)
                    )
                    station_song = StationSong.objects.create(
                        song=song, 
                        index=station.songs.count()
                    )
                    station.songs.add(station_song)
                    station.save()
                    break
                except:
                    print "SoundCloud fail >.<" + str(track)
    return station.pk


def play_station(station_id):
    resp = twilio.twiml.Response()
    station = Station.objects.get(pk=station_id)
    song_to_play = station.songs.get(index=station.current_song)
    print "SONG TO PLAY:", song_to_play
    with resp.gather(action="/controls", numDigits=1) as g:
        g.say("Playing " + song_to_play.song.title)
        print song_to_play.url
        g.play(song_to_play.url)
    resp.redirect(url="/controls", method="GET")
    return resp


@twilio_view
def controls(request):    
    if request.method == 'POST':
        from_number = request.POST.get('From', None)
        num = int(request.POST.get('Digits', 0))
    elif request.method == 'GET':
        from_number = request.GET.get('From', None)
        num = 6
    account = Account.objects.get(phone_number=from_number)
    station = account.current_station

    if num == 0:
        return save(station)
    elif num == 1:
        return dislike(station)
    elif num == 4:
        return previous_track(station)
    else:
        return next_track(station)


def get_artists(genre):
    host = "api.spotify.com/v1/search"
    url = "https://{0}?".format(host)
    params = {
        "q": "* genre:\"{0}\"".format(genre),
        "type": "artist",
        "limit": 10
    }
    headers = { "User-Agent": "Mozilla/5.0" }
    response = requests.get(url, params=params, headers=headers)
    json_response = json.loads(response.content)
    artists = json_response['artists']['items']
    return artists


def previous_track(station):
    if station.current_song > 0:
        station.current_song -= 1
        station.save()
    return play_station(station.pk)


def next_track(station):
    station.current_song += 1
    station.save()
    return play_station(station.pk)


def dislike(station):
    station_song = station.songs.get(index=station.current_song)
    station.disliked_songs.add(station_song.song)
    station.save()
    remove_disliked_song(station)
    return play_station(station.pk)


def remove_disliked_song(station):
    station.songs.get(index=station.current_song).delete()
    for i in range(station.current_song + 1, station.songs.count() + 1):
        song = station.songs.get(index=i)
        song.index -= 1
        song.save()
    station.save()


def save(station):
    resp = twilio.twiml.Response()
    resp.say("Enter %04d # next time to start where you left off or share with \
              your friends" % (station.pk))
    return resp