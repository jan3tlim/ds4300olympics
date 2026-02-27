"""
Olympics Analysis Using MongoDB

Contributions:
Amelia converted the CSV files to JSON and then wrote this file to import the data from
olympics.json programmatically.
Katie & Janet reviewed the code.
"""
from pymongo import MongoClient
import json

# Create client
client = MongoClient()
client.drop_database('olympics')

# Create / connect to database
db = client['olympics']

# Initiate collections
events = db.events
athletes = db.athletes
countries = db.countries
games = db.games
results = db.results

# Clear old collections
events.drop()
athletes.drop()
countries.drop()
games.drop()
results.drop()


# Load JSON file
with open('olympics.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Insert each collection
if 'athletes' in data:
    athletes.insert_many(data['athletes'])
    print("Inserted athletes:", len(data['athletes']))

if 'events' in data:
    events.insert_many(data['events'])
    print("Inserted events:", len(data['events']))

if 'countries' in data:
    countries.insert_many(data['countries'])
    print("Inserted countries:", len(data['countries']))

if 'games' in data:
    games.insert_many(data['games'])
    print("Inserted games:", len(data['games']))

if 'results' in data:
    results.insert_many(data['results'])
    print("Inserted results:", len(data['results']))

# Print collections
print("\nCollections in DB:")
print(db.list_collection_names())

# Print sample of each collection
print("\nSample athlete:")
print(athletes.find_one())

print("\nSample event:")
print(events.find_one())

print("\nSample country:")
print(countries.find_one())

print("\nSample game:")
print(games.find_one())

print("\nSample results:")
print(results.find_one())