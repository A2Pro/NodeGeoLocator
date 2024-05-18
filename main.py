import os
from flask import Flask, render_template
from dotenv import load_dotenv

app = Flask(__name__)

@app.route("/map")
def map():
    coordinates = []
    with open("coordinates.txt") as file:
        for line in file:
            ip, lat, lng = line.strip().split(" | ")
            coordinates.append({"ip": ip, "lat": lat, "lng": lng})
    return render_template("index.html", coordinates=coordinates)

if __name__ == "__main__":
    app.run(debug=True)
