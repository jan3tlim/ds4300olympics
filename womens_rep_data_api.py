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

class WomensRepDataAPI:

    def __init__(self, db_name="olympics"):
        client = MongoClient()
        self.db = client[db_name]
        self.games = self.db.games
        self.athletes = self.db.athletes

    def female_athlete_ids(self):
        """
        Returns a set of all female athlete_ids from the athletes collection
        """
        return {
            doc["athlete_id"]
            for doc in self.athletes.find({"sex": "F"}, {"athlete_id": 1, "_id": 0})
        }

    def base_pipeline(self, season=None, year=None):
        """
        I was struggling writing this code to be more concise. AI suggested I use a base_pipeline
        function since most of my functions start with the same steps.
        Shared pipeline: optional match → unwind athletes → filter to females
        """
        female_ids = self.female_athlete_ids()
        match = {}

        # Filtering by the seasons and years
        if season:
            match["season"] = season
        if year:
            match["year"] = year
        pipeline = []
        if match:
            pipeline.append({"$match": match})
        # Using unwind so that every document represents one female athlete in
        # one event in one game
        pipeline += [
            {"$unwind": "$athletes"},
            {"$match": {"athletes.athlete_id": {"$in": list(female_ids)}}},
        ]
        return pipeline

    def female_athletes_year(self, season=None):
        """
        Returns the total number of unique female athletes per year
        """
        pipeline = self.base_pipeline(season=season) + [
            {"$group": {"_id": {"year": "$year", "athlete_id": "$athletes.athlete_id"}}},
            {"$group": {"_id": "$_id.year", "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}},
            {"$project": {"_id": 0, "year": "$_id", "count": 1}},
        ]
        results = list(self.games.aggregate(pipeline))
        # Make sure the order is year, count
        return [{"year": d["year"], "count": d["count"]} for d in results]

    def female_athletes_events(self, season=None, year=None, top_n=None, bottom_n=None):
        """
        Returns total unique female athletes per event across all years
        """
        pipeline = self.base_pipeline(season=season, year=year) + [
            {"$unwind": "$athletes.events"},
            {"$group": {"_id": {"event": "$athletes.events", "athlete_id": "$athletes.athlete_id"}}},
            {"$group": {"_id": "$_id.event", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$project": {"_id": 0, "event": "$_id", "count": 1}},
        ]
        # Make sure the order is event, count
        results = [{"event": d["event"], "count": d["count"]} for d in self.games.aggregate(pipeline)]

        if top_n:
            return results[:top_n]
        # I chose not to visualize the bottom_n but left this code to display that it could be easily done
        if bottom_n:
            return results[-bottom_n:]
        return results

    def female_athlete_event_growth(self, top_n=None):
        """
        Returns events with the largest increase in female athletes from that events
        first Olympic appearance to most recent
        AI was super helpful in helping me to brainstorm how to go about this pipeline,
        fixing my syntax, and debugging
        """
        pipeline = self.base_pipeline() + [
            {"$unwind": "$athletes.events"},
            # So that we are not counting athletes twice
            {"$group": {
                "_id": {"event": "$athletes.events", "year": "$year", "athlete_id": "$athletes.athlete_id"}
            }},
            # Counts how many unique female athletes competed in that event in that year
            {"$group": {
                "_id": {"event": "$_id.event", "year": "$_id.year"},
                "count": {"$sum": 1}
            }},
            # Collects all the yearly counts into an array (yearly_counts)
            {"$group": {
                "_id": "$_id.event",
                "yearly_counts": {"$push": {"year": "$_id.year", "count": "$count"}}
            }},
            # Sorts yearly_counts by year and takes first and last entries
            {"$project": {
                "event": "$_id",
                "first": {"$first": {"$sortArray": {"input": "$yearly_counts", "sortBy": {"year": 1}}}},
                "last": {"$last": {"$sortArray": {"input": "$yearly_counts", "sortBy": {"year": 1}}}},
            }},
            # Displaying data and computing growth
            {"$project": {
                "_id": 0,
                "event": 1,
                "first_year": "$first.year",
                "last_year": "$last.year",
                "first_count": "$first.count",
                "last_count": "$last.count",
                "growth": {"$subtract": ["$last.count", "$first.count"]},
            }},
            # At first, I was going to take a growth percentage. However, the percentages ended up being
            # so large that it was too difficult to interpret. Therefore, I decided to keep the raw
            # increase in number of female athletes
            {"$sort": {"growth": -1}},
        ]
        if top_n:
            pipeline.append({"$limit": top_n})
        return list(self.games.aggregate(pipeline))