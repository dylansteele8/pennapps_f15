from flask import Flask
import twilio.twiml
from pymongo import MongoClient
 
app = Flask(__name__)
 
@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    # Get the caller's phone number from the incoming Twilio request
    from_number = request.values.get('From', None)

    client = MongoClient()
    db = client.test

    result = db.test.insert_one(
    {
        "address": {
            "street": "2 Avenue",
            "zipcode": "10075",
            "building": "1480",
            "coord": [-73.9557413, 40.7720266]
        },
        "borough": "Manhattan",
        "cuisine": "Italian",
        "grades": [
            {
                "grade": "A",
                "score": 11
            },
            {
                "grade": "B",
                "score": 17
            }
        ],
        "name": "Vella",
        "restaurant_id": "41704620"
    }
)
    
    # Respond to incoming requests
    resp = twilio.twiml.Response()
    if from_number in db.test.find():
        # Greet the caller by name
        resp.say("Hello " + callers[from_number])
    else:
        resp.say("Hello Monkey")
 
    return str(resp)
 
if __name__ == "__main__":
    app.run(debug=True)