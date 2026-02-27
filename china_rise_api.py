"""
Olympics Analysis Using MongoDB
Contributions: Janet wrote the entirety of this API. Amelia & Katie reviewed the code.

China's Rise as an Olympic Superpower API:
    To analyze China's meteoric rise in Olympic performance from 1984 to present.
    Questions:
    1. How many medals has China won, filtered by type, sport, or season?
    2. Which sports has China been most dominant in?
    3. How has China's medal count changed over time?
    4. How does China compare to other major Olympic nations?
"""
from typing import List, Dict, Any, Optional
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["olympics"]


def get_china_medals(
    medal_type: Optional[str] = None,
    sport: Optional[str] = None,
    season: Optional[str] = None
) -> Dict[str, Any]:
    """
    Returns China's medal counts, optionally filtered by medal type, sport, and/or season.

    How it works:
    - Builds a match filter for CHN with optional medal_type, sport, and season
    - Runs three queries: total count, breakdown by medal type, and top events
    - Returns a combined summary dict

    Parameters:
        medal_type: "Gold", "Silver", or "Bronze"
        sport: e.g., "Swimming", "Diving", "Gymnastics"
        season: "Summer" or "Winter"

    Returns:
        dict with total medals, gold/silver/bronze breakdown, and top 5 events
    """
    match_filter: Dict[str, Any] = {"noc": "CHN"}
    if medal_type:
        match_filter["medal"] = medal_type
    if sport:
        match_filter["sport"] = sport
    if season:
        match_filter["season"] = season

    # Total count with all filters applied
    total = db.results.count_documents(match_filter)

    # Breakdown by medal type (without medal_type filter so we always see all three)
    breakdown_filter: Dict[str, Any] = {"noc": "CHN"}
    if sport:
        breakdown_filter["sport"] = sport
    if season:
        breakdown_filter["season"] = season

    breakdown = list(db.results.aggregate([
        {"$match": breakdown_filter},
        {"$group": {"_id": "$medal", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]))

    # Top 5 events by medal count
    top_events = list(db.results.aggregate([
        {"$match": match_filter},
        {"$group": {"_id": "$event", "medals": {"$sum": 1}}},
        {"$sort": {"medals": -1}},
        {"$limit": 5}
    ]))

    return {
        "filters": {"medal_type": medal_type, "sport": sport, "season": season},
        "total_medals": total,
        "breakdown": {item["_id"]: item["count"] for item in breakdown},
        "top_events": [{"event": e["_id"], "medals": e["medals"]} for e in top_events]
    }


def get_china_top_sports(top_n: int = 10) -> List[Dict[str, Any]]:
    """
    Returns China's most successful sports ranked by total medal count.

    How it works:
    - Filters results to CHN
    - Groups by sport, counting total medals and using $cond to count each medal type
    - Sorts by total descending and limits to top_n

    Parameters:
        top_n: number of sports to return (default 10)

    Returns:
        list of dicts with sport name, total, gold, silver, and bronze counts
    """
    pipeline = [
        {"$match": {"noc": "CHN"}},

        # Count total and each medal type using conditional sums
        {"$group": {
            "_id": "$sport",
            "total": {"$sum": 1},
            "gold": {"$sum": {"$cond": [{"$eq": ["$medal", "Gold"]}, 1, 0]}},
            "silver": {"$sum": {"$cond": [{"$eq": ["$medal", "Silver"]}, 1, 0]}},
            "bronze": {"$sum": {"$cond": [{"$eq": ["$medal", "Bronze"]}, 1, 0]}}
        }},

        # Most medals first
        {"$sort": {"total": -1}},
        {"$limit": top_n}
    ]
    return list(db.results.aggregate(pipeline))


def get_china_medal_trends(
    start_year: Optional[int] = None,
    end_year: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Returns China's medal count per Olympic year, optionally within a year range.

    How it works:
    - Filters results to CHN with optional year range
    - Groups by year and season, summing medals
    - Projects clean output and sorts chronologically

    Parameters:
        start_year: earliest year to include
        end_year: latest year to include

    Returns:
        list of dicts with year, season, and medal count
    """
    match_filter: Dict[str, Any] = {"noc": "CHN"}
    if start_year or end_year:
        match_filter["year"] = {}
        if start_year:
            match_filter["year"]["$gte"] = start_year
        if end_year:
            match_filter["year"]["$lte"] = end_year

    pipeline = [
        {"$match": match_filter},

        # Group by year and season to separate Summer/Winter
        {"$group": {
            "_id": {"year": "$year", "season": "$season"},
            "medals": {"$sum": 1}
        }},

        # Flatten the _id fields into top-level keys
        {"$project": {
            "year": "$_id.year",
            "season": "$_id.season",
            "medals": 1,
            "_id": 0
        }},

        # Chronological order
        {"$sort": {"year": 1}}
    ]
    return list(db.results.aggregate(pipeline))


def compare_china_vs(noc_list: List[str]) -> List[Dict[str, Any]]:
    """
    Compares China's medal performance against other countries.

    How it works:
    - Combines CHN with the provided list of NOCs
    - Uses $in to match all relevant countries in one query
    - Groups by NOC with conditional sums for each medal type
    - Sorts by total medals descending

    Parameters:
        noc_list: list of NOC codes to compare against (e.g., ["USA", "GBR", "JPN"])

    Returns:
        list of dicts with country, total, gold, silver, and bronze counts
    """
    all_nocs = ["CHN"] + [n.upper() for n in noc_list]
    pipeline = [
        # Match China and all comparison countries
        {"$match": {"noc": {"$in": all_nocs}}},

        # Count total and each medal type per country
        {"$group": {
            "_id": "$noc",
            "total": {"$sum": 1},
            "gold": {"$sum": {"$cond": [{"$eq": ["$medal", "Gold"]}, 1, 0]}},
            "silver": {"$sum": {"$cond": [{"$eq": ["$medal", "Silver"]}, 1, 0]}},
            "bronze": {"$sum": {"$cond": [{"$eq": ["$medal", "Bronze"]}, 1, 0]}}
        }},

        # Most medals first
        {"$sort": {"total": -1}}
    ]
    return list(db.results.aggregate(pipeline))


# === Test the API ===
if __name__ == "__main__":
    print("=== China Overall Medal Summary ===")
    result = get_china_medals()
    print(f"Total: {result['total_medals']}")
    print(f"Breakdown: {result['breakdown']}")
    print(f"Top events: {result['top_events']}\n")

    print("=== China's Gold Medals in Diving ===")
    result = get_china_medals(medal_type="Gold", sport="Diving")
    print(f"Total: {result['total_medals']}")
    print(f"Top events: {result['top_events']}\n")

    print("=== China's Top 10 Sports ===")
    for s in get_china_top_sports():
        print(f"{s['_id']}: {s['total']} medals ({s['gold']}G {s['silver']}S {s['bronze']}B)")
    print()

    print("=== China Medal Trends ===")
    for t in get_china_medal_trends():
        print(t)
    print()

    print("=== China vs USA, GBR, JPN ===")
    for c in compare_china_vs(["USA", "GBR", "JPN"]):
        print(c)