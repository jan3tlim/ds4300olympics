import csv
import json

# ── CONFIG ────────────────────────────────────────────────────────────────
FILES = ["olympics.tsv", "olympics_2022.tsv"]
COUNTRY_FILE = "country-information.tsv"
OUTPUT_FILE = "olympics.json"

# ── UTILITY FUNCTIONS ─────────────────────────────────────────────────────
def read_tsv(filepath):
    with open(filepath, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))

def clean(val):
    if val is None:
        return None
    v = val.strip()
    return None if v in ("NA", "") else v

def to_int(val):
    v = clean(val)
    try:
        return int(v) if v else None
    except ValueError:
        return None

def to_float(val):
    v = clean(val)
    try:
        return float(v) if v else None
    except ValueError:
        return None

# ── LOAD DATA ─────────────────────────────────────────────────────────────
rows = []
for f in FILES:
    rows.extend(read_tsv(f))
country_rows = read_tsv(COUNTRY_FILE)

# ── 1. ATHLETES COLLECTION ─────────────────────────────────────────────────
athletes = {}
for r in rows:
    aid = r["athlete_id"].strip()
    if aid not in athletes:
        athletes[aid] = {
            "athlete_id": aid,
            "name": clean(r["name"]),
            "sex": clean(r["sex"]),
            "birth_year": to_int(r["birth_year"]),
            "birth_day": clean(r["birth_day"]),
            "birth_place": clean(r["birth_place"]),
            "height_cm": to_float(r["height"]),
            "weight_kg": to_float(r["weight"]),
            "nocs": set(),
            "teams": set(),
            "events": set(),
        }
    athletes[aid]["nocs"].add(r["noc"].strip())
    if clean(r["team"]):
        athletes[aid]["teams"].add(clean(r["team"]))
    if clean(r["event"]):
        athletes[aid]["events"].add(clean(r["event"]))

athlete_collection = []
for a in athletes.values():
    a["nocs"] = sorted(a["nocs"])
    a["teams"] = sorted(a["teams"])
    a["events"] = sorted(a["events"])
    athlete_collection.append(a)
athlete_collection.sort(key=lambda x: x["athlete_id"])

# ── 2. COUNTRIES COLLECTION ────────────────────────────────────────────────
country_collection = []
for r in country_rows:
    noc = clean(r.get("NOC"))
    if not noc:
        continue
    country_collection.append({
        "noc": noc,
        "official_name": clean(r.get("official_name_en")),
        "continent": clean(r.get("Continent")),
        "capital": clean(r.get("Capital")),
    })

# ── 3. EVENTS COLLECTION ───────────────────────────────────────────────────
events = {}
for r in rows:
    event = clean(r["event"])
    sport = clean(r["sport"])
    if not event:
        continue
    if event not in events:
        events[event] = {
            "event_name": event,
            "sport": sport,
            "games_held_in": set(),
        }
    events[event]["games_held_in"].add(clean(r["games"]))

event_collection = []
for e in events.values():
    e["games_held_in"] = sorted(e["games_held_in"])
    event_collection.append(e)
event_collection.sort(key=lambda x: x["event_name"])

# ── 4. GAMES COLLECTION ────────────────────────────────────────────────────
games = {}
for r in rows:
    g = clean(r["games"])
    if not g:
        continue
    if g not in games:
        games[g] = {
            "games": g,
            "year": to_int(r["year"]),
            "season": clean(r["season"]),
            "city": clean(r["city"]),
            "events": set(),
            "athletes": {},          # { athlete_id -> {name, events: set()} }
            "medal_results": [],
            "_medal_set": set(),
        }
    gd = games[g]
    event = clean(r["event"])
    aid = r["athlete_id"].strip()
    medal = clean(r["medal"])

    if event:
        gd["events"].add(event)

    # ── athlete-event linkage ──────────────────────────────────────────
    if aid not in gd["athletes"]:
        gd["athletes"][aid] = {"name": clean(r["name"]), "events": set()}
    if event:
        gd["athletes"][aid]["events"].add(event)

    if medal:
        key = (aid, event, medal)
        if key not in gd["_medal_set"]:
            gd["_medal_set"].add(key)
            gd["medal_results"].append({
                "athlete_id": aid,
                "athlete_name": clean(r["name"]),
                "event": event,
                "medal": medal,
            })

games_collections = []
for gd in games.values():
    gd["events"] = sorted(gd["events"])
    # Serialize athletes dict → list with events as sorted list
    gd["athletes"] = [
        {"athlete_id": aid, "name": info["name"], "events": sorted(info["events"])}
        for aid, info in sorted(gd["athletes"].items())
    ]
    gd["medal_results"].sort(key=lambda x: (x["event"] or "", x["medal"] or ""))
    del gd["_medal_set"]
    games_collections.append(gd)
games_collections.sort(key=lambda x: (x["year"] or 0, x["season"] or ""))

# ── 5. RESULTS COLLECTION ─────────────────────────────────────────────────
result_set = set()
results_collection = []

for r in rows:
    medal = clean(r["medal"])
    if not medal:
        continue

    aid = r["athlete_id"].strip()
    event = clean(r["event"])
    games_name = clean(r["games"])
    noc = clean(r["noc"])

    key = (aid, event, games_name, medal)
    if key in result_set:
        continue
    result_set.add(key)

    results_collection.append({
        "athlete_id": aid,
        "athlete_name": clean(r["name"]),
        "sex": clean(r["sex"]),
        "noc": noc,
        "games": games_name,
        "year": to_int(r["year"]),
        "season": clean(r["season"]),
        "sport": clean(r["sport"]),
        "event": event,
        "medal": medal,
    })

results_collection.sort(key=lambda x: (x["year"] or 0, x["games"] or "", x["event"] or ""))

# ── 6. WRITE JSON ─────────────────────────────────────────────────────────
output = {
    "athletes": athlete_collection,
    "countries": country_collection,
    "events": event_collection,
    "games": games_collections,
    "results": results_collection,
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"Done! Written to {OUTPUT_FILE}")
print(f"  Athletes:  {len(athlete_collection)}")
print(f"  Countries: {len(country_collection)}")
print(f"  Events:    {len(event_collection)}")
print(f"  Games:     {len(games_collections)}")
print(f"  Results:   {len(results_collection)}")