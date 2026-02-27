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
        """Line graph of total female athletes per year (all Olympics)."""
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
        """Line graph comparing female athletes per year: Summer vs Winter."""
        summer = self.data.female_athletes_year(season="Summer")
        winter = self.data.female_athletes_year(season="Winter")

        plt.figure(figsize=(12, 5))
        plt.plot([d["year"] for d in summer], [d["count"] for d in summer],
                 marker="o", linewidth=2, label="Summer")
        plt.plot([d["year"] for d in winter], [d["count"] for d in winter],
                 marker="o", linewidth=2, label="Winter")
        plt.title("Female Athletes: Summer vs Winter Olympics")
        plt.xlabel("Year")
        plt.ylabel("Number of Female Athletes")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_top_female_events(self, top_n=10):
        """
        Side-by-side horizontal bar charts: top N events overall,
        in 2020 Summer, and in 2022 Winter.
        """
        overall   = self.data.female_athletes_events(top_n=top_n)
        summer_20 = self.data.female_athletes_events(season="Summer", year=2020, top_n=top_n)
        winter_22 = self.data.female_athletes_events(season="Winter", year=2022, top_n=top_n)

        fig, axes = plt.subplots(1, 3, figsize=(20, 7))
        datasets = [
            (overall,   "Top 10 Female Events (All Time)"),
            (summer_20, "Top 10 Female Events – 2020 Summer"),
            (winter_22, "Top 10 Female Events – 2022 Winter"),
        ]
        for ax, (data, title) in zip(axes, datasets):
            events = [d["event"] for d in data]
            counts = [d["count"] for d in data]
            bars = ax.barh(events[::-1], counts[::-1], color="#d94f70")
            ax.set_title(title, fontsize=11, fontweight="bold")
            ax.set_xlabel("Number of Female Athletes")
            ax.bar_label(bars, padding=3, fontsize=8)
            ax.margins(x=0.15)
            ax.grid(axis="x", linestyle="--", alpha=0.5)

        plt.suptitle("Female Athlete Representation by Event", fontsize=14, fontweight="bold", y=1.01)
        plt.tight_layout()
        plt.show()

    def plot_event_growth_bar(self, top_n=None):
        """
        Horizontal bar chart of top N events by absolute growth in female athletes
        (most recent count minus first appearance count).
        """
        data = self.data.female_athlete_event_growth(top_n=top_n)
        data = [d for d in data if d["growth"] > 0 and d["first_year"] and d["last_year"]]
        data = sorted(data, key=lambda x: x["growth"])  # ascending so largest is at top

        events = [d["event"] for d in data]
        growth = [d["growth"] for d in data]

        fig, ax = plt.subplots(figsize=(12, 7))
        bars = ax.barh(events, growth, color="#d94f70")
        ax.bar_label(bars, labels=[f"+{g}" for g in growth], padding=4, fontsize=9)
        ax.set_xlabel("Growth in Female Athletes (first → most recent Olympics)")
        ax.set_title("Top 10 Events by Female Athlete Growth",
                     fontsize=13, fontweight="bold")
        ax.margins(x=0.12)
        ax.grid(axis="x", linestyle="--", alpha=0.4)
        ax.spines[["top", "right"]].set_visible(False)
        plt.tight_layout()
        plt.show()