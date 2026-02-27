"""
Olympics Analysis Using MongoDB
Contributions: Janet wrote the entirety of this visualization. Amelia & Katie reviewed the code.

Visualizing China's Rise as an Olympic Superpower!
Shows how China's medals break down by sport over time,
revealing strategic investment in specific sports.
"""
from china_rise_api import get_china_top_sports
from pymongo import MongoClient
import matplotlib.pyplot as plt

client = MongoClient("mongodb://localhost:27017/")
db = client["olympics"]


def get_china_sport_trends(top_n: int = 6):
    """
    Helper: get China's medal counts per year for each of their top sports.

    How it works:
    - First finds China's top_n most successful sports
    - Then for each sport, groups medals by year
    - Returns a dict mapping sport name to (years, medals) tuples
    """
    top_sports = get_china_top_sports(top_n=top_n)
    sport_names = [s["_id"] for s in top_sports]

    trends = {}
    for sport in sport_names:
        pipeline = [
            {"$match": {"noc": "CHN", "sport": sport, "season": "Summer"}},
            {"$group": {"_id": "$year", "medals": {"$sum": 1}}},
            {"$sort": {"_id": 1}}
        ]
        results = list(db.results.aggregate(pipeline))
        years = [r["_id"] for r in results]
        medals = [r["medals"] for r in results]
        if years:
            trends[sport] = (years, medals)

    return trends


def plot_china_sport_breakdown():
    """
    Line chart showing how China's medals break down by sport over time.
    Reveals which sports drove China's rise at different points in history.

    How it works:
    - Gets medal trends for China's top 6 sports
    - Builds a unified year axis across all sports
    - Plots a line for each sport with distinct colors
    - Annotates Beijing 2008 as a key milestone
    """
    trends = get_china_sport_trends(top_n=6)

    # Build a unified set of years across all sports
    all_years = sorted(set(y for years, _ in trends.values() for y in years))

    # For each sport, fill in 0 for years with no medals
    sport_data = {}
    for sport, (years, medals) in trends.items():
        medal_map = dict(zip(years, medals))
        sport_data[sport] = [medal_map.get(y, 0) for y in all_years]

    # Colors for each sport
    colors = ["#e63946", "#457b9d", "#2a9d8f", "#e9c46a", "#f4a261", "#264653"]

    fig, ax = plt.subplots(figsize=(14, 7))

    # Line chart for each sport
    for (sport, data), color in zip(sport_data.items(), colors):
        ax.plot(all_years, data, label=sport, color=color,
                linewidth=2.5, marker="o", markersize=4)

    # Emphasize Beijing 2008
    if 2008 in all_years:
        max_2008 = max(data[all_years.index(2008)] for data in sport_data.values())
        ax.annotate("Beijing 2008\n(Host nation)",
                    xy=(2008, max_2008),
                    xytext=(2012, max_2008 + 10),
                    arrowprops=dict(arrowstyle="->", color="black", lw=1.5),
                    fontsize=10, fontweight="bold")

    ax.set_title("China's Olympic Medal Breakdown by Sport\n"
                 "Summer Games (1984–2024)",
                 fontsize=15, fontweight="bold")
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Total Medals Won", fontsize=12)
    ax.legend(loc="upper left", fontsize=10, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("report/china_sport_breakdown.png", dpi=150)
    plt.show()
    print("Saved to report/china_sport_breakdown.png")


if __name__ == "__main__":
    plot_china_sport_breakdown()