"""
Olympics Analysis Using MongoDB

Contributions:
Amelia wrote the code to implement the API she wrote on WomensRepAPI
Katie wrote the code to implement the API she wrote on EventDiversityAPI
Janet wrote the code to implement the API she wrote on ChinaRiseAPI

"""
from womens_rep_data_api import WomensRepDataAPI
from womens_rep_plot_api import WomensRepPlotAPI
from event_div_api import EventDiversityAPI
event_div = EventDiversityAPI()
womens_rep_data = WomensRepDataAPI()
womens_rep_plot = WomensRepPlotAPI()

# AI suggested using tabulate to make the outputs more readable
from tabulate import tabulate

def main():

    # Display data to explore female representation at the Olympics
    female_athletes_year_data = womens_rep_data.female_athletes_year()
    print("\nNumber of Female Athletes per Year:")
    print(tabulate(female_athletes_year_data, headers="keys", tablefmt="pretty"))

    top_female_events_data = womens_rep_data.female_athletes_events(top_n=10)
    print("\nTop 10 events with female athletes across per Year:")
    print(tabulate(top_female_events_data, headers="keys", tablefmt="pretty"))

    female_athlete_growth_data = womens_rep_data.female_athlete_event_growth(top_n=10)
    print("\nTop 10 Events with Largest Female Athlete Growth:")
    print(tabulate(female_athlete_growth_data, headers="keys", tablefmt="pretty"))

    # Plot all charts to visualize data about female representation
    womens_rep_plot.plot_female_athletes_year()
    womens_rep_plot.plot_female_athletes_seasons()
    womens_rep_plot.plot_top_female_events(top_n=10)
    womens_rep_plot.plot_event_growth_bar(top_n=20)

    # Display data to explore event diversity
    print("\nTop 20 Athletes by Event Count:")
    print(tabulate(event_div.top_athletes_by_event_count(top_n=20), headers="keys", tablefmt="pretty"))

    print("\nTop 20 Events by Unique Athlete Count:")
    print(tabulate(event_div.top_events_by_athlete_count(top_n=20), headers="keys", tablefmt="pretty"))
    event_div.plot_top_events_by_athlete_count(top_n=10)

    print("\nAverage Event Count by Sex:")
    print(tabulate(event_div.avg_event_count_by_sex(), headers="keys", tablefmt="pretty"))

    print("\nTop 20 NOCs by Event Diversity:")
    print(tabulate(event_div.top_nocs_by_event_diversity(top_n=20), headers="keys", tablefmt="pretty"))

if __name__ == "__main__":
    main()