"""
Olympics Analysis Using MongoDB

Contributions:
Amelia wrote the code to implement the API she wrote on  WomensRepAPI
Katie:
Janet:
"""

from womens_rep_api import WomensRepAPI
am_api = WomensRepAPI()

def main():

    """
    Calls WomensRepAPI() to women's representation in the Olympics over the years and across events
    """
    events = am_api.results.distinct("event")
    print(sorted(events))
    print(f"Total distinct events: {len(events)}")

    #year_data = am_api.female_athletes_year()
    #print(year_data[:10])

    # Plot
    #plot_female_athletes_year = am_api.plot_female_athletes_year()
    #plot_female_athletes_seasons = am_api.plot_female_athletes_seasons()

    #top_female_events = am_api.female_athletes_events(top_n=10)
    #print("Top 10 events:", top_female_events)

    #female_athlete_growth = am_api.female_athlete_event_growth(top_n=10)
    #print(female_athlete_growth)

    events = am_api.results.distinct("event")
    print(sorted(events))
    print(f"Total distinct events: {len(events)}")

if __name__ == "__main__":
    main()

