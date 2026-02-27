"""
Olympics Analysis Using MongoDB

Contributions:
Amelia converted the CSV files to JSON and then wrote this file to import the data from
olympics.json programmatically.
Katie & Janet reviewed the code.
"""
from pymongo import MongoClient
import json

def main():

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

    # Load JSON file
    with open('olympics.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Insert each collection
    collections = {
        'athletes': athletes,
        'events': events,
        'countries': countries,
        'games': games,
        'results': results,
        }

    # Load each collection
    # Before, I wrote out "if" statements for each collection. AI helped me streamline this
    for name, collection in collections.items():
        if name in data:
            collection.insert_many(data[name])
            print(f"Inserted {name}: {len(data[name])}")

    # Print collections in DB to verify
    print("\nCollections in DB:")
    print(db.list_collection_names())

    # Print a sample document from each collection
    for name, collection in collections.items():
        print(f"\nSample {name[:-1]}:")
        print(collection.find_one())

if __name__ == "__main__":
    main()