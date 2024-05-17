import requests
import os
from dotenv import load_dotenv

load_dotenv
API_KEY = os.getenv("GEOIPLOCATOR_API_KEY")


def get_coords(ip):
    response = requests.get(f'https://api.ipgeolocation.io/ipgeo?apiKey=7f52e57f64904bcaa6c5bca14fd0a27f&ip={ip}')
    json = response.json()
    lat = 0
    print(json)
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
    with open('ip_addresses.txt') as file:
        print()
        ips = [line.strip() for line in file.readlines()]
    
   
    for ip in ips:
        coords = get_coords(ip)
        y+=1
        if(coords["lat"]!=0 or coords["lng"]!=0):
            x+=1
            with open("coordinates.txt", "a") as file:
                file.write(f'{ip} | {coords["lat"]} | {coords["lng"]} \n')
            print(f'{x} found in {y}')
            
        
        

main()

# we can get rid of development once I get a google maps API key, / implement it (i already have one)