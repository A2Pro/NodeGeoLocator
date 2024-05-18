import requests
import os
from dotenv import load_dotenv

load_dotenv()

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

if __name__ == "__main__":
    main()
