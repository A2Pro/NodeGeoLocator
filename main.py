from flask import Flask, render_template
from dotenv import load_dotenv
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

uri = os.getenv("MONGO_URI")


client = MongoClient(uri, server_api=ServerApi('1'))

def get_file(filename):
    collection = client["ip_coords"]["ip/coords"]
    entry  = collection.find_one({"filename": filename})
    return entry["file"]

@app.route("/map")
def map():
    coordinates = []
    with open("coordinates.txt", "w") as file:
        file.write(get_file("coordinates.txt"))
    with open("coordinates.txt") as file:
        for line in file:
            ip, lat, lng = line.strip().split(" | ")
            coordinates.append({"ip": ip, "lat": lat, "lng": lng})
    return render_template("index.html", coordinates=coordinates)

if __name__ == "__main__":
    app.run(debug=True)
