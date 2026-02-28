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
from china_rise_api import (
    get_china_medals,
    get_china_top_sports,
    get_china_medal_trends,
    compare_china_vs
)
from china_visualization import plot_china_sport_breakdown

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

    # Display data to explore China's rise as an Olympic superpower
    print("\n=== China Overall Medal Summary ===")
    result = get_china_medals()
    summary_data = [{"Total Medals": result["total_medals"], **result["breakdown"]}]
    print(tabulate(summary_data, headers="keys", tablefmt="pretty"))

    print("\nChina's Top 5 Events (Overall):")
    print(tabulate(result["top_events"], headers="keys", tablefmt="pretty"))

    print("\nChina's Gold Medals in Diving:")
    diving_result = get_china_medals(medal_type="Gold", sport="Diving")
    print(f"Total: {diving_result['total_medals']}")
    print(tabulate(diving_result["top_events"], headers="keys", tablefmt="pretty"))

    print("\nChina's Top 10 Sports:")
    top_sports_data = [
        {"Sport": s["_id"], "Total": s["total"], "Gold": s["gold"],
         "Silver": s["silver"], "Bronze": s["bronze"]}
        for s in get_china_top_sports()
    ]
    print(tabulate(top_sports_data, headers="keys", tablefmt="pretty"))

    print("\nChina Medal Trends Over Time:")
    trends_data = [
        {"Year": t["year"], "Season": t["season"], "Medals": t["medals"]}
        for t in get_china_medal_trends()
    ]
    print(tabulate(trends_data, headers="keys", tablefmt="pretty"))

    print("\nChina vs USA, GBR, JPN:")
    comparison_data = [
        {"Country": c["_id"], "Total": c["total"], "Gold": c["gold"],
         "Silver": c["silver"], "Bronze": c["bronze"]}
        for c in compare_china_vs(["USA", "GBR", "JPN"])
    ]
    print(tabulate(comparison_data, headers="keys", tablefmt="pretty"))

    # Plot China's sport breakdown visualization
    plot_china_sport_breakdown()

if __name__ == "__main__":
    main()
