"""
Olympics Analysis Using MongoDB

Contributions:
Amelia wrote the code to implement the API she wrote on  WomensRepAPI and the associated visualizations
Katie wrote the code to implement the API she wrote on EventDiversity and the associated visualization
Janet:
"""

from womens_rep_data_api import WomensRepDataAPI
from womens_rep_plot_api import WomensRepPlotAPI
from katie_api import EventDiversityAPI
from viz_katie import plot_events_uniq_athletes
womens_rep_data = WomensRepDataAPI()
womens_rep_plot = WomensRepPlotAPI()
event_diversity = EventDiversityAPI()


# AI suggested using tabulate to make the outputs more readable
from tabulate import tabulate

def main():

    #WomensRepData 
    female_athletes_year_data = womens_rep_data.female_athletes_year()
    print("\nNumber of Female Athletes per Year:")
    print(tabulate(female_athletes_year_data, headers="keys", tablefmt="pretty"))

    top_female_events_data = womens_rep_data.female_athletes_events(top_n=10)
    print("\nTop 10 events with female athletes across per Year:")
    print(tabulate(top_female_events_data, headers="keys", tablefmt="pretty"))

    female_athlete_growth_data = womens_rep_data.female_athlete_event_growth(top_n=10)
    print("\nTop 10 Events with Largest Female Athlete Growth:")
    print(tabulate(female_athlete_growth_data, headers="keys", tablefmt="pretty"))

    # Plot all charts to visualize above data
    womens_rep_plot.plot_female_athletes_year()
    womens_rep_plot.plot_female_athletes_seasons()
    womens_rep_plot.plot_top_female_events(top_n=10)
    womens_rep_plot.plot_event_growth_bar(top_n=20)

    #EventDiversity
    top_athletes_data = event_diversity_api.top_athletes_by_event_count(top_n=5)
    print("\nTop 5 Athletes by Event Count:")
    print(tabulate(top_athletes_data, headers="keys", tablefmt="pretty"))

    top_events_data = event_diversity_api.top_events_by_athlete_count(top_n=5)
    print("\nTop 5 Events by Unique Athlete Count:")
    print(tabulate(top_events_data, headers="keys", tablefmt="pretty"))

    avg_by_sex_data = event_diversity_api.avg_event_count_by_sex()
    print("\nAverage Event Count per Athlete by Sex:")
    print(tabulate(avg_by_sex_data, headers="keys", tablefmt="pretty"))

    top_nocs_data = event_diversity_api.top_nocs_by_event_diversity(top_n=10)
    print("\nTop 10 NOCs by Event Diversity:")
    print(tabulate(top_nocs_data, headers="keys", tablefmt="pretty"))

    # Plot chart for "Which events have the most unique athletes?"
    plot_events_uniq_athletes()


if __name__ == "__main__":
    main()

