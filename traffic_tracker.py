from data import messages, secrets
from datetime import datetime
import random
import requests
import sms
from time import sleep

# API rate limit: 40 requests per minute, 2000 requests per day
# 1 request every 43.2 seconds

body = {"coordinates": [secrets.coordinates['work'], secrets.coordinates['home']], 'preference': 'fastest'}

headers = {
  'Accept': 'application/json; charset=utf-8',
  'Authorization': secrets.directions_api_key,
  'Content-Type': 'application/json; charset=utf-8'
}

consecutive_errors = 0

while True:
  sleep(60)

  try:
    response = requests.post('https://api.openrouteservice.org/v2/directions/driving-car/json', json=body, headers=headers)
    response.raise_for_status()
  except requests.exceptions.RequestException as e:
    consecutive_errors += 1
    if consecutive_errors >= 5:
      print(f'Error retrieving directions: {e}')
      exit(2)
    continue

  consecutive_errors = 0

  duration_minutes = int(response.json()['routes'][0]['summary']['duration'] / 60)

  if duration_minutes <= 35:
    sms.send(random.choice(messages.short_duration_messages(duration_minutes)))
    print("Notification sent. Exiting...")
    exit(0)

  current_time = datetime.now()
  seven_pm = current_time.replace(hour=19, minute=0, second=0, microsecond=0)
  if current_time >= seven_pm:
    sms.send(random.choice(messages.long_duration_messages(duration_minutes)))
    print("Notification sent. Exiting...")
    exit(1)
