"""
Olympics Analysis Using MongoDB
Contributions: Katie wrote the entirety of this API. Amelia & Janet reviewed the code.

Visualizing Event Diversity API! Visualizes question 2 (Which events have the most unique athletes?) from API. 
"""

import matplotlib.pyplot as plt
from katie_api import EventDiversityAPI


def main():
    api = EventDiversityAPI(db_name="olympics", collection_name="athletes")

    top_n = 10
    data = api.top_events_by_athlete_count(top_n=top_n)

    # reversed so that top event is at the top of the chart for aesthetic and readability purposes
    data = list(reversed(data))

    events = [d["event"] for d in data]
    counts = [d["unique_athletes"] for d in data]

    plt.figure(figsize=(10, 6))
    plt.barh(events, counts, color = "indigo")
    plt.title(f"Top {top_n} Events by Unique Athlete Participation")
    plt.xlabel("Number of Unique Athletes")
    plt.ylabel("Event")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()