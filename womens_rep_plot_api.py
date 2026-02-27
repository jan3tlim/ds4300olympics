"""
Olympics Analysis Using MongoDB
Contributions: Amelia wrote the entirety of this API. Katie & Janet reviewed the code.

Visualizing Women's Representation API! Focused on growth of female athletes overall,
broken out by year, season, and event.
"""
from womens_rep_data_api import WomensRepDataAPI
import matplotlib.pyplot as plt

class WomensRepPlotAPI:

    def __init__(self, db_name="olympics"):
        self.data = WomensRepDataAPI(db_name)

    def plot_female_athletes_year(self):
        """
        Line graph of total female athletes per year (all Olympics)
        """
        d = self.data.female_athletes_year()
        plt.figure(figsize=(12, 5))
        plt.plot([x["year"] for x in d], [x["count"] for x in d], marker="o", linewidth=2)
        plt.title("Female Athletes in the Olympics Over Time")
        plt.xlabel("Year")
        plt.ylabel("Number of Female Athletes")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_female_athletes_seasons(self):
        """
        Line graph comparing female athletes in Summer vs. Winter Olympics
        """
        summer = self.data.female_athletes_year(season="Summer")
        winter = self.data.female_athletes_year(season="Winter")

        plt.figure(figsize=(12, 5))
        plt.plot([d["year"] for d in summer], [d["count"] for d in summer],
                 marker="o", linewidth=2, label="Summer")
        plt.plot([d["year"] for d in winter], [d["count"] for d in winter],
                 marker="o", linewidth=2, label="Winter")
        plt.title("Female Athletes in the Summer vs Winter Olympics Over Time")
        plt.xlabel("Year")
        plt.ylabel("Number of Female Athletes")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_top_female_events(self, top_n=None):
        """
        3 Horizontal bar charts:
        1. Top 10 events with greatest number of female athletes
        2. Top 10 events with greatest number of female athletes in the
            most recent Summer Olympics (Tokyo 2020)
        3. Top 10 events with greatest number of female athletes in the
            most recent Winter Olympics (Beijing 2022)
        """
        # Define 3 bar charts
        overall = self.data.female_athletes_events(top_n=top_n)
        summer_20 = self.data.female_athletes_events(season="Summer", year=2020, top_n=top_n)
        winter_22 = self.data.female_athletes_events(season="Winter", year=2022, top_n=top_n)

        fig, axes = plt.subplots(1, 3, figsize=(20, 7))
        datasets = [
            # Giving each chart a different color
            (overall, "Top 10 Events with Female Athletes (All Time)", "pink"),
            (summer_20, "Top 10 Events with Female Athletes – 2020 Summer", "green"),
            (winter_22, "Top 10 Events with Female Athletes – 2022 Winter", "teal"),
        ]
        for ax, (data, title, color) in zip(axes, datasets):
            events = [d["event"] for d in data]
            counts = [d["count"] for d in data]
            bars = ax.barh(events[::-1], counts[::-1], color=color)
            ax.set_title(title, fontsize=10, fontweight="bold", wrap=True)
            ax.set_xlabel("Number of Female Athletes")
            ax.bar_label(bars, padding=3, fontsize=8)
            ax.margins(x=0.15)
            ax.grid(axis="x", linestyle="--", alpha=0.5)

        plt.suptitle("Female Athlete Representation by Event", fontsize=14, fontweight="bold")
        # The title was being cut off so AI suggested to keep the top 5% reserved for the title
        # so that the charts don't cut it off
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()

    def plot_event_growth_bar(self, top_n=None):
        """
        Bar chart of top 10 events that have grown in
        the number of female athletes
        (most recent count minus first appearance count)
        """
        data = self.data.female_athlete_event_growth(top_n=top_n)
        data = [d for d in data if d["growth"] > 0 and d["first_year"] and d["last_year"]]
        # Descending order so largest is on the left
        data = sorted(data, key=lambda x: x["growth"], reverse=True)

        events = [d["event"] for d in data]
        growth = [d["growth"] for d in data]

        fig, ax = plt.subplots(figsize=(12, 7))
        bars = ax.bar(events, growth, color="red")
        ax.bar_label(bars, labels=[f"+{g}" for g in growth], padding=4, fontsize=9)
        ax.set_ylabel("Growth in Female Athletes (first → most recent Olympics)")
        ax.set_title("Top 10 Events by Female Athlete Growth",
                     fontsize=13, fontweight="bold")
        ax.margins(y=0.12)
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        ax.spines[["top", "right"]].set_visible(False)
        plt.xticks(rotation=45, ha="right", fontsize=8)
        plt.tight_layout()
        plt.show()