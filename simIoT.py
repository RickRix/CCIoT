import time
import random
import requests
import geocoder

FIREBASE_URL = "https://test-96269-default-rtdb.asia-southeast1.firebasedatabase.app/bin_status.json"

def get_bin_level():
    """ Simulates ultrasonic sensor readings (distance in cm). """
    return random.randint(0, 100)  # Random fill percentage (0-100%)

def get_live_location():
    """ Gets live location (latitude, longitude) using geocoder. """
    location = geocoder.ip("me")
    return location.latlng if location.latlng else [0, 0]

def send_data_to_firebase(bin_level, location):
    """ Sends bin level & location data to Firebase Realtime Database. """
    data = {
        "Bin_Level": bin_level,
        "Latitude": location[0],
        "Longitude": location[1],
        "Status": "Full" if bin_level > 75 else "Not Full",
        "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    response = requests.put(FIREBASE_URL, json=data)
    
    if response.status_code == 200:
        print(f"Data sent: {data}")
    else:
        print(f"Failed to send data. Error: {response.text}")

# Simulate bin level updates every 10 seconds
while True:
    bin_level = get_bin_level()
    location = get_live_location()
    
    print(f"Bin Level: {bin_level}%, Location: {location}")
    send_data_to_firebase(bin_level, location)
    
    # Trigger alert if bin is full
    if bin_level > 75:
        print("ALERT: The bin is full! Please empty it.")
    
    time.sleep(10)