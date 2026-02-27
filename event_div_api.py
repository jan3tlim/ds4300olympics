
"""
Olympics Analysis Using MongoDB
Contributions: Katie wrote the entirety of this API. Amelia & Janet reviewed the code.

Event Diversity & Specialization API:
    To learn how broadly athletes (and countries) participate across different Olympic events.


    Questions: (used AI to come up with questions given my topic of event diversity)
    1) Which athletes competed in the most events?
    2) Which events have the most unique athletes?
    3) Do women or men tend to compete in more events per athlete?
    4) Which countries have the broadest event participation?
"""

from typing import List, Dict, Any, Optional
from pymongo import MongoClient
import matplotlib.pyplot as plt


class EventDiversityAPI:

    def __init__(self, db_name: str = "olympics", collection_name: str = "athletes"):
        client = MongoClient()
        self.db = client[db_name]
        self.athletes = self.db[collection_name]

    def base_pipeline(
            self,
            sex: Optional[str] = None,
            noc: Optional[str] = None,
            min_birth_year: Optional[int] = None,
            max_birth_year: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Took advice from Amelia and created a base_pipeline function for simplification
        Shared pipeline: optional $match on sex → optional $match on NOC (via nocs array) →
          optional birth year range filter → return filtered athlete documents

        Parameters:
          sex: filter to "M" or "F"
          noc: filter to athletes who have a specific noc inside their nocs list
          min_birth_year / max_birth_year: optional birth year range filters

        Returns:
          A list of MongoDB aggregation stages (pipeline) starting with $match.
        """

        match: Dict[str, Any] = {}

        # If sex is provided, match exactly
        if sex is not None:
            match["sex"] = sex

        # If noc is provided, match documents where the nocs array contains said value
        if noc is not None:
            match["nocs"] = noc

            # Birth year filters (only add if provided)
        if min_birth_year is not None or max_birth_year is not None:
            birth_year_filter: Dict[str, Any] = {}
            if min_birth_year is not None:
                birth_year_filter["$gte"] = min_birth_year
            if max_birth_year is not None:
                birth_year_filter["$lte"] = max_birth_year
            match["birth_year"] = birth_year_filter

        pipeline: List[Dict[str, Any]] = []
        if match:
            pipeline.append({"$match": match})

        return pipeline

    def top_athletes_by_event_count(
            self,
            top_n: int = 20,
            sex: Optional[str] = None,
            noc: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Returns the athletes who participated in the most events.

        How it works:
        - Filter (optional)
        - Compute number of events as length of events array using $size
        - Sort by that count descending
        - Limit to top_n
        """

        pipeline = self.base_pipeline(sex=sex, noc=noc) + [
            {"$addFields": {"event_count": {"$size": "$events"}}},

            {"$project": {
                "_id": 0,
                "athlete_id": 1,
                "name": 1,
                "sex": 1,
                "nocs": 1,
                "birth_year": 1,
                "event_count": 1
            }},

            # Sort by event_count (largest first)
            {"$sort": {"event_count": -1}},

            # Only keep the top N to get athelete with most events
            {"$limit": top_n},
        ]

        return list(self.athletes.aggregate(pipeline))

    def top_events_by_athlete_count(
            self,
            top_n: int = 20,
            sex: Optional[str] = None,
            noc: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Returns events that show up for the most unique athletes.

        How it works:
        - Filter (optional)
        - $unwind events: turns each athlete document into multiple rows (one per event)
        - Group by event, counting distinct athlete_ids
        - Sort and limit
        """

        pipeline = self.base_pipeline(sex=sex, noc=noc) + [
            {"$unwind": "$events"},

            # Count unique athletes per event: use $addToSet to build a set of athlete_ids for each event
            {"$group": {
                "_id": "$events",
                "athletes": {"$addToSet": "$athlete_id"}
            }},

            # Convert set size to a number
            {"$project": {
                "_id": 0,
                "event": "$_id",
                "unique_athletes": {"$size": "$athletes"}
            }},

            {"$sort": {"unique_athletes": -1}},
            {"$limit": top_n},
        ]

        return list(self.athletes.aggregate(pipeline))

    def avg_event_count_by_sex(self) -> List[Dict[str, Any]]:
        """
        Compares men vs women: average number of events per athlete.

        How it works:
        - Compute event_count per athlete
        - Group by sex and average event_count
        """

        pipeline = [
            {"$addFields": {"event_count": {"$size": "$events"}}},

            {"$group": {
                "_id": "$sex",
                "avg_events_per_athlete": {"$avg": "$event_count"},
                "min_events": {"$min": "$event_count"},
                "max_events": {"$max": "$event_count"},
                "athletes": {"$sum": 1}
            }},

            {"$project": {
                "_id": 0,
                "sex": "$_id",
                "avg_events_per_athlete": {"$round": ["$avg_events_per_athlete", 2]},
                "min_events": 1,
                "max_events": 1,
                "athletes": 1
            }},

            {"$sort": {"sex": 1}}
        ]

        return list(self.athletes.aggregate(pipeline))

    def top_nocs_by_event_diversity(self, top_n: int = 20) -> List[Dict[str, Any]]:
        """
        Returns NOCs (countries) ranked by how many distinct events their athletes participated in.

        How it works:
        - $unwind nocs: athlete may have multiple NOCs
        - $unwind events: one row per (noc, event) per athlete
        - Group by noc, collect distinct events using $addToSet
        - Rank by the size of that set
        """

        pipeline = [
            {"$unwind": "$nocs"},
            {"$unwind": "$events"},

            {"$group": {
                "_id": "$nocs",
                "events": {"$addToSet": "$events"},
                "athletes": {"$addToSet": "$athlete_id"}
            }},

            {"$project": {
                "_id": 0,
                "noc": "$_id",
                "unique_events": {"$size": "$events"},
                "unique_athletes": {"$size": "$athletes"},
            }},

            {"$sort": {"unique_events": -1}},
            {"$limit": top_n},
        ]

        return list(self.athletes.aggregate(pipeline))

    def plot_top_events_by_athlete_count(self, top_n: int = 10) -> None:
        """
        Horizontal bar chart of top N events by unique athlete participation.
        """
        data = self.top_events_by_athlete_count()
        # Reversed so that top event is at the top of the chart for aesthetic and readability
        data = list(reversed(data))

        events = [d["event"] for d in data]
        counts = [d["unique_athletes"] for d in data]

        plt.figure(figsize=(10, 6))
        plt.barh(events, counts, color="indigo")
        plt.title(f"Top {top_n} Events by Unique Athlete Participation")
        plt.xlabel("Number of Unique Athletes")
        plt.ylabel("Event")
        plt.tight_layout()
        plt.show()