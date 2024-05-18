import requests
import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

uri = os.getenv("MONGO_URI")

client = MongoClient(uri, server_api=ServerApi('1'))

def get_file(filename):
    collection = client["ip_coords"]["ip/coords"]
    entry  = collection.find_one({"filename": filename})
    return entry["file"]

def update_file(filename):
    f = open(filename, "r")
    file_content = f.read()
    collection = client["ip_coords"]["ip/coords"]
    collection.update_one(
      { "filename" : filename },
      { "$set": { "file" : file_content} } #void
    )

API_KEY = os.getenv("GEOIPLOCATOR_API_KEY")

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

def main():
    x = 0
    y = 0
    ips = []
    with open("coordinates.txt", "w") as file:
        file.write(get_file("coordinates.txt"))
    with open("coordinates.txt", "r") as file:
        coords_list = file.read()
    with open('ip_addresses.txt') as file:
        ips = [line.strip() for line in file.readlines()]
    filtered_ips = [ip for ip in ips if ip not in coords_list]
    for ip in filtered_ips:
        coords = get_coords(ip)
        y += 1
        if coords["lat"] != 0 or coords["lng"] != 0:
            x += 1
            with open("coordinates.txt", "a") as file:
                file.write(f'{ip} | {coords["lat"]} | {coords["lng"]} \n')
            print(f'{x} found in {y}')
    update_file("coordinates.txt", "coordinates.txt")
    

if __name__ == "__main__":
    main()
