from django.shortcuts import render

from twilio import twiml
from django_twilio.decorators import twilio_view

# Create your views here.

def home(request):
    data = {}
    return render(request, 'base.html', data)

@twilio_view
def process(request):
    print request
    resp = twilio.twiml.Response()
    resp.say("Hello Monkey")
    return str(resp)

    # Get the caller's phone number from the incoming Twilio request
    from_number = request.values.get('From', None)

    client = MongoClient()
    db = client.accounts
    resp = twilio.twiml.Response()

    # Respond to incoming requests
    if db.accounts.find({"phone_number": from_number }):
        resp.say("Welcome back")
        resp.say(resume_play(from_number))
    else:
        resp.say("Let's begin")
        result = db.test.insert_one(
            {
                "phone_number": from_number
            }
        )
        resp.say(start_play())

    return str(resp)