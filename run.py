from flask import Flask
import twilio.twiml
from pymongo import MongoClient
 
app = Flask(__name__)
 
@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
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
 
if __name__ == "__main__":
    app.run(debug=True)

# {
#     "address": {
#         "street": "2 Avenue",
#         "zipcode": "10075",
#         "building": "1480",
#         "coord": [-73.9557413, 40.7720266]
#     },
#     "borough": "Manhattan",
#     "cuisine": "Italian",
#     "grades": [
#         {
#             "grade": "A",
#             "score": 11
#         },
#         {
#             "grade": "B",
#             "score": 17
#         }
#     ],
#     "name": "Vella",
#     "restaurant_id": "41704620"
# }