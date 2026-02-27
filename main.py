"""
Olympics Analysis Using MongoDB

Contributions:
Amelia wrote the code to implement the API she wrote on  WomensRepAPI
Katie:
Janet:
"""

from womens_rep_data_api import WomensRepDataAPI
from womens_rep_plot_api import WomensRepPlotAPI
womens_rep_data = WomensRepDataAPI()
womens_rep_plot = WomensRepPlotAPI()

def main():

    """
    Calls WomensRepAPI() to women's representation in the Olympics over the years and across events
    """
    #year_data = womens_rep_data.female_athletes_year()
    #print(year_data[:10])

    #top_female_events = womens_rep_data.female_athletes_events(top_n=10)
    #print("Top 10 events:", top_female_events)

    #female_athlete_growth = womens_rep_data.female_athlete_event_growth(top_n=10)
    #print(female_athlete_growth)

    # Plot
    #plot_female_athletes_year = womens_rep_plot.plot_female_athletes_year()
    #plot_female_athletes_seasons = womens_rep_plot.plot_female_athletes_seasons()

    # Q1: Has the overall number of female athletes increased?
    womens_rep_plot.plot_female_athletes_year()

    # Q2: Summer vs Winter comparison
    womens_rep_plot.plot_female_athletes_seasons()

    # Q3: Events with most female athletes (all time, 2020 Summer, 2022 Winter)
    womens_rep_plot.plot_top_female_events(top_n=10)

    # Q4: Events with most absolute growth
    womens_rep_plot.plot_event_growth_bar(top_n=20)

if __name__ == "__main__":
    main()

