"""
Olympics Analysis Using MongoDB
Contributions: Amelia wrote the entirety of this API. Katie & Janet reviewed the code.

Women's Representation API:
    To learn more about how women's representation in the Olympics over the years (1896-2022).
    Questions:
    1. Has the overall number of female athletes increased or decreased?
    2. Does the total number of female athletes differ significantly between summer vs. winter olympics?
    3. What events see the greatest number of female athletes overall? What events see the lowest?
    4. What events have seen the most growth in female athletes?
"""
from pymongo import MongoClient


class WomensRepAPI:

    def __init__(self, db_name="olympics"):
        client = MongoClient()
        self.db = client[db_name]
        self.results = self.db.results

    def female_athletes_year(self, season=None):
        """
        Returns the total number of unique female athletes per year.
        Optional: filter by season ("Summer" or "Winter").
        Output: [{year: int, count: int}, ...]
        """
        match = {"sex": "F"}

        if season:
            match["season"] = season

        pipeline = [
            {"$match": match},
            # Count distinct athlete_ids per year to avoid double-counting
            # athletes who competed in multiple events the same year
            {"$group": {"_id": {"year": "$year", "athlete_id": "$athlete_id"}}},
            {"$group": {"_id": "$_id.year", "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}},
            {"$project": {"_id": 0, "year": "$_id", "count": 1}},
        ]
        return list(self.results.aggregate(pipeline))

    def female_athletes_seasons(self):
        """
        LOWK not super helpful ...
        Returns female athlete counts per year for Summer and Winter.
        Output: {"Summer": [{year, count}], "Winter": [{year, count}]}
        """
        return {
            "Summer": self.female_athletes_year(season="Summer"),
            "Winter": self.female_athletes_year(season="Winter"),
        }

    def female_athletes_by_event(self, season=None, top_n=None, bottom_n=None):
        """
        Returns total number of female athletes per event across all years.
        Output: [{event: str, count: int}, ...]
        """
        match = {"sex": "F"}
        if season:
            match["season"] = season

        pipeline = [
            {"$match": match},
            {"$group": {"_id": "$event", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$project": {"_id": 0, "event": "$_id", "count": 1}},
        ]
        results = list(self.results.aggregate(pipeline))

        if top_n:
            return results[:top_n]
        if bottom_n:
            return results[-bottom_n:]
        return results

    def female_athlete_growth_by_event(self, top_n=10):
        """
        Returns top N events with the largest increase in female athletes
        from their first to most recent Olympic appearance.
        Output: [{event, first_year, last_year, growth}, ...]
        """
        pipeline = [
            {"$match": {"sex": "F"}},
            {"$group": {
                "_id": {"event": "$event", "year": "$year"},
                "count": {"$sum": 1}
            }},
            {"$group": {
                "_id": "$_id.event",
                "yearly_counts": {"$push": {"year": "$_id.year", "count": "$count"}}
            }},
            {"$project": {
                "event": "$_id",
                "first": {"$first": {"$sortArray": {"input": "$yearly_counts", "sortBy": {"year": 1}}}},
                "last": {"$last": {"$sortArray": {"input": "$yearly_counts", "sortBy": {"year": 1}}}},
            }},
            {"$project": {
                "_id": 0,
                "event": 1,
                "first_year": "$first.year",
                "last_year": "$last.year",
                "growth": {"$subtract": ["$last.count", "$first.count"]},
            }},
            {"$sort": {"growth": -1}},
            {"$limit": top_n},
        ]
        return list(self.results.aggregate(pipeline))