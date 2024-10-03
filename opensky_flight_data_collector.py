import requests
import csv
import time
from datetime import datetime
import pandas as pd

# OpenSky States API URL
url = "https://opensky-network.org/api/states/all"

# File where data will be saved
csv_filename = 'opensky_flights_60min.csv'

# Create and write header to the CSV file
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['icao24', 'callsign', 'latitude', 'longitude', 'altitude', 'velocity', 'timestamp'])

# Collect data every 30 seconds for 60 minutes
for i in range(120):  
    print(f"Performing query {i+1}...")

    # Send API request with authentication (use username and password if needed)
    response = requests.get(url, auth=('username', 'password'))

    if response.status_code == 200:
        data = response.json()

        total_flights = len(data['states'])
        num_flights_to_sample = 300

        # Sample the first 300 flights or fewer if available
        if total_flights >= num_flights_to_sample:
            sampled_flights = data['states'][:num_flights_to_sample]
        else:
            sampled_flights = data['states']

        # Append flight data to the CSV file
        with open(csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)

            for flight in sampled_flights:
                icao24 = flight[0]    
                callsign = flight[1]  
                longitude = flight[5] 
                latitude = flight[6]  
                altitude = flight[7]  
                velocity = flight[9]  
                timestamp = datetime.utcfromtimestamp(data['time']).strftime('%Y-%m-%d %H:%M:%S')  

                writer.writerow([icao24, callsign, latitude, longitude, altitude, velocity, timestamp])

        print(f"{num_flights_to_sample} flight records saved.")

    else:
        print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
    
    # Wait for 30 seconds before the next request
    time.sleep(30)

print(f"Data collection completed. Results saved to '{csv_filename}'.")

# Read the collected data
df = pd.read_csv('opensky_flights_60min.csv')

# Remove rows with missing values
icao24_with_missing_values = df[df.isnull().any(axis=1)]['icao24'].unique()
df_cleaned = df[~df['icao24'].isin(icao24_with_missing_values)]

# Remove aircrafts with fewer than 120 records
icao24_counts = df_cleaned['icao24'].value_counts()
icao24_less_than_120 = icao24_counts[icao24_counts < 120].index
df_final = df_cleaned[~df_cleaned['icao24'].isin(icao24_less_than_120)]

# Save cleaned data to a new CSV file
df_final.to_csv('flights_data.csv', index=False)
