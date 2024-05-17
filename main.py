from flask import Flask, render_template
import requests
import os
from dotenv import load_dotenv

load_dotenv
API_KEY = os.getenv("GEOIPLOCATOR_API_KEY")

app = Flask(__name__)

def get_coords(ip):
    response = requests.get(f'https://api.ipgeolocation.io/ipgeo?apiKey={API_KEY}&ip={ip}')
    json = response.json()
    lat = 0
    long = 0
    try:
        lat = json["latitude"]
        long = json["longitude"]
    except:
        pass
    return {"lat": lat, "lng": long}

@app.route("/")
def main():
    ips = []
    with open('ip_addresses.txt') as file:
        print()
        ips = [line.strip() for line in file.readlines()]
    
    coordinates = [get_coords(ip) for ip in ips]
    
    return render_template("index.html", coordinates=coordinates)

if __name__ == "__main__":
    app.run(debug=True)
