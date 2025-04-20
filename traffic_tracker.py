from data import messages, secrets
from datetime import datetime
import random
import requests
import sms
from time import sleep

# API restrictions:
# - 20,000 queries per month to remain in the free tier
# - rate limit of 3,000 queries per minute
# - maximum allowed number of intermediate waypoints per ComputeRoutes request is 25

url = 'https://routes.googleapis.com/directions/v2:computeRoutes'

headers = {
  'Content-Type': 'application/json',
  'X-Goog-Api-Key': secrets.routes_api_key,
  'X-Goog-FieldMask': 'routes.duration'
}

payload = {
  'origin': {
    'address': secrets.addresses['work']
  },
  'destination': {
    'address': secrets.addresses['home']
  },
  'travelMode': 'DRIVE',
  'routingPreference': 'TRAFFIC_AWARE_OPTIMAL',
  'computeAlternativeRoutes': False,
  'routeModifiers': {
    'avoidTolls': False,
    'avoidHighways': False,
    'avoidFerries': False
  },
  'languageCode': 'en-US'
}

consecutive_errors = 0

while True:
  sleep(60)

  try:
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
  except Exception as e:
    consecutive_errors += 1
    if consecutive_errors >= 5:
      print(f'Error retrieving directions: {e}')
      exit(2)
    continue

  consecutive_errors = 0

  duration_minutes = int(response.json()['routes'][0]['duration'][:-1]) // 60
  if duration_minutes <= 30:
    sms.send(random.choice(messages.short_duration_messages(duration_minutes)), secrets.recipient_phone_numbers[0])
    sms.send(messages.notification_message(duration_minutes), secrets.recipient_phone_numbers[1])
    print("Notification sent. Exiting...")
    exit(0)

  current_time = datetime.now()
  seven_thirty_pm = current_time.replace(hour=18, minute=30, second=0, microsecond=0)
  if current_time >= seven_thirty_pm:
    sms.send(random.choice(messages.long_duration_messages(duration_minutes)), secrets.recipient_phone_numbers[0])
    sms.send(messages.notification_message(duration_minutes), secrets.recipient_phone_numbers[1])
    print("Notification sent. Exiting...")
    exit(1)
