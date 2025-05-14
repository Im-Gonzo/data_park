
# Kafka Event Generator for VPN Security Events

## Task Description
Create a data generator that produces realistic VPN connection events and sends them to Kafka.
This will provide the streaming data needed for the Spark Structured Streaming challenges.

## Setup

```python
import json
import random
import time
from datetime import datetime
from kafka import KafkaProducer

# Configure the Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Kafka topic
TOPIC = 'vpn_connection_events'
```

## Generate Realistic VPN Events

```python
# Configuration data
COUNTRIES = [
    "US", "UK", "DE", "FR", "JP", "AU", "CA", "BR", "IN", "RU", 
    "CN", "SG", "NL", "ES", "IT", "SE", "NO", "FI", "DK", "PL"
]

DEVICE_TYPES = [
    "Windows PC", "MacBook", "iPhone", "Android Phone", "iPad", 
    "Android Tablet", "Linux Server", "Linux Desktop", "Windows Server", "IoT Device"
]

CONNECTION_STATUSES = ["successful", "failed_password", "failed_network", "timeout", "rate_limited"]

# Distribution weights
MOBILE_DEVICES = ["iPhone", "Android Phone", "iPad", "Android Tablet"]
STATUS_WEIGHTS = [0.85, 0.06, 0.04, 0.03, 0.02]  # 85% success rate

# List of users (100 sample users)
USERS = [f"user_{i:03d}" for i in range(1, 101)]

# Some users for targeted anomaly generation
SUSPICIOUS_USERS = USERS[90:95]    # Users that will exhibit suspicious behavior
VIP_USERS = USERS[0:10]            # High-volume legitimate users
```

## Event Generation Functions

```python
def generate_normal_event():
    """Generate a normal VPN connection event"""
    user_id = random.choice(USERS)
    
    # Determine user's "home" country
    # In a real scenario, most users connect from a limited set of countries
    user_id_num = int(user_id.split('_')[1])
    user_country_index = user_id_num % 5  # Each user has ~5 common countries
    common_countries = COUNTRIES[user_country_index:user_country_index+5]
    
    return {
        "user_id": user_id,
        "timestamp": datetime.now().isoformat(),
        "country": random.choice(common_countries),
        "device_type": random.choice(DEVICE_TYPES),
        "connection_status": random.choices(CONNECTION_STATUSES, weights=STATUS_WEIGHTS)[0],
        "connection_id": f"conn_{random.randint(10000, 99999)}",
        "ip_address": f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}",
        "vpn_server": f"server-{random.randint(1, 50)}",
        "protocol": random.choice(["UDP", "TCP"])
    }

def generate_country_hopping_event(user_id):
    """Generate an event where a user connects from unusual countries"""
    event = generate_normal_event()
    event["user_id"] = user_id
    event["country"] = random.choice(COUNTRIES)  # Any random country
    return event

def generate_brute_force_event(user_id):
    """Generate failed login attempts"""
    event = generate_normal_event()
    event["user_id"] = user_id
    event["connection_status"] = "failed_password"
    return event
```

## Main Event Generation Loop

```python
def start_event_generation(duration_seconds=300, events_per_second=5):
    """Generate events and send to Kafka for a specified duration"""
    start_time = time.time()
    event_count = 0
    
    try:
        while time.time() - start_time < duration_seconds:
            # Determine what type of event to generate
            rand_val = random.random()
            
            if rand_val < 0.05 and random.random() < 0.3:  # 5% chance of suspicious events, 30% of those are country hopping
                # Generate country hopping (multiple countries in short time)
                user = random.choice(SUSPICIOUS_USERS)
                for _ in range(random.randint(3, 5)):
                    event = generate_country_hopping_event(user)
                    producer.send(TOPIC, event)
                    event_count += 1
                    time.sleep(0.2)  # Short delay between country hops
                    
            elif rand_val < 0.05:  # Remaining suspicious events are brute force
                # Generate brute force attempt
                user = random.choice(SUSPICIOUS_USERS)
                for _ in range(random.randint(5, 10)):
                    event = generate_brute_force_event(user)
                    producer.send(TOPIC, event)
                    event_count += 1
                    time.sleep(0.1)  # Quick succession of failed attempts
                    
            else:
                # Generate normal event
                event = generate_normal_event()
                producer.send(TOPIC, event)
                event_count += 1
            
            # Sleep to control event rate
            sleep_time = 1.0 / events_per_second
            time.sleep(sleep_time)
            
            # Print progress
            if event_count % 50 == 0:
                elapsed = time.time() - start_time
                print(f"Generated {event_count} events in {elapsed:.2f} seconds")
                
        print(f"Event generation complete. Total events: {event_count}")
            
    except KeyboardInterrupt:
        print(f"Event generation stopped. Total events: {event_count}")
    finally:
        producer.flush()
        
# Start generating events
if __name__ == "__main__":
    print("Starting VPN event generator...")
    print(f"Sending events to Kafka topic: {TOPIC}")
    print("Press Ctrl+C to stop")
    
    start_event_generation(duration_seconds=3600, events_per_second=10)
```

## Testing Notes
- Make sure Kafka is running before starting the generator
- Monitor Kafka topic to ensure events are being produced
- Adjust event rate as needed for your testing
