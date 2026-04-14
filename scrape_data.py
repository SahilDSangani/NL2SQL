# =============================================================================
# scrape_data.py — Download MLB pitching and fielding stats
# =============================================================================
# HOW TO RUN:
#   python3 scrape_data.py
#
#   No extra dependencies — uses only requests and pandas (already installed).
#
# This produces two files in the same directory:
#   pitching.csv  — pitcher-season rows, 2010–2024
#   fielding.csv  — fielder-position-season rows, 2010–2024
#
# After running, reload everything into the database:
#   python3 ingest_data.py
#
# Data source:
#   Official MLB Stats API (statsapi.mlb.com) — free, no auth required.
#   Uses the same player IDs (mlbID) as the existing batting data.
# =============================================================================

import time
import requests
import pandas as pd

START_YEAR = 2010
END_YEAR   = 2024
PAGE_SIZE  = 2000   # max rows per API request
SLEEP_SEC  = 0.5    # pause between requests to be polite

BASE       = "https://statsapi.mlb.com/api/v1/stats"
TEAMS_URL  = "https://statsapi.mlb.com/api/v1/teams?sportId=1"

# ---------------------------------------------------------------------------
# Team abbreviation lookup
# ---------------------------------------------------------------------------

def load_team_abbreviations() -> dict[int, str]:
    """Returns {team_id: abbreviation} for all current MLB teams."""
    r = requests.get(TEAMS_URL, timeout=15)
    if r.status_code != 200:
        return {}
    return {t["id"]: t["abbreviation"] for t in r.json().get("teams", [])}


# ---------------------------------------------------------------------------
# API helper
# ---------------------------------------------------------------------------

def fetch_splits(group: str, season: int) -> list[dict]:
    """
    Fetch all stat splits for a given group ('pitching' or 'fielding')
    and season year. Paginates automatically.
    """
    splits = []
    offset = 0
    while True:
        params = {
            "stats":      "season",
            "group":      group,
            "season":     season,
            "playerPool": "all",
            "limit":      PAGE_SIZE,
            "offset":     offset,
        }
        r = requests.get(BASE, params=params, timeout=30)
        if r.status_code != 200:
            raise RuntimeError(f"HTTP {r.status_code} for {group} {season} offset={offset}")

        data  = r.json().get("stats", [{}])[0]
        page  = data.get("splits", [])
        total = data.get("totalSplits", 0)
        splits.extend(page)

        offset += PAGE_SIZE
        if offset >= total:
            break
        time.sleep(SLEEP_SEC)

    return splits


# ---------------------------------------------------------------------------
# Pitching
# ---------------------------------------------------------------------------

def scrape_pitching(team_abbr: dict) -> pd.DataFrame:
    """
    Fetches season pitching totals for all MLB pitchers, 2010–2024.

    Output columns (snake_cased from API, then renamed to match batting.csv style):
      Name, mlbID, Tm, Year, Age,
      W, L, ERA, G, GS, CG, SHO, SV, SVO, HLD, BS,
      IP, H, R, ER, HR, BB, IBB, SO, HBP, WP, BK,
      WHIP, H9, HR9, BB9, SO9, BF
    """
    rows = []
    for year in range(START_YEAR, END_YEAR + 1):
        print(f"  Pitching {year}...", end=" ", flush=True)
        splits = fetch_splits("pitching", year)
        for s in splits:
            stat   = s.get("stat", {})
            player = s.get("player", {})
            team   = s.get("team", {})
            rows.append({
                "Name":  player.get("fullName"),
                "mlbID": player.get("id"),
                "Tm":    team_abbr.get(team.get("id"), team.get("name")),
                "Year":  year,
                "Age":   stat.get("age"),
                "W":     stat.get("wins"),
                "L":     stat.get("losses"),
                "ERA":   stat.get("era"),
                "G":     stat.get("gamesPitched"),
                "GS":    stat.get("gamesStarted"),
                "CG":    stat.get("completeGames"),
                "SHO":   stat.get("shutouts"),
                "SV":    stat.get("saves"),
                "SVO":   stat.get("saveOpportunities"),
                "HLD":   stat.get("holds"),
                "BS":    stat.get("blownSaves"),
                "IP":    stat.get("inningsPitched"),
                "H":     stat.get("hits"),
                "R":     stat.get("runs"),
                "ER":    stat.get("earnedRuns"),
                "HR":    stat.get("homeRuns"),
                "BB":    stat.get("baseOnBalls"),
                "IBB":   stat.get("intentionalWalks"),
                "SO":    stat.get("strikeOuts"),
                "HBP":   stat.get("hitByPitch"),
                "WP":    stat.get("wildPitches"),
                "BK":    stat.get("balks"),
                "WHIP":  stat.get("whip"),
                "H9":    stat.get("hitsPer9Inn"),
                "HR9":   stat.get("homeRunsPer9"),
                "BB9":   stat.get("walksPer9Inn"),
                "SO9":   stat.get("strikeoutsPer9Inn"),
                "BF":    stat.get("battersFaced"),
            })
        time.sleep(SLEEP_SEC)
        print(f"{len(splits)} rows")

    df = pd.DataFrame(rows)
    print(f"  Total: {len(df)} pitcher-season rows")
    return df


# ---------------------------------------------------------------------------
# Fielding
# ---------------------------------------------------------------------------

def scrape_fielding(team_abbr: dict) -> pd.DataFrame:
    """
    Fetches season fielding totals for all MLB players, 2010–2024.
    One row per player-position-season (a player who played multiple
    positions gets one row per position).

    Output columns:
      Name, mlbID, Tm, Year, POS, Age,
      G, GS, Inn, PO, A, E, DP, FP,
      RF9 (range factor per 9 inn), RFG (range factor per game)
    """
    rows = []
    for year in range(START_YEAR, END_YEAR + 1):
        print(f"  Fielding {year}...", end=" ", flush=True)
        splits = fetch_splits("fielding", year)
        for s in splits:
            stat     = s.get("stat", {})
            player   = s.get("player", {})
            team     = s.get("team", {})
            position = s.get("position", {})
            rows.append({
                "Name":  player.get("fullName"),
                "mlbID": player.get("id"),
                "Tm":    team_abbr.get(team.get("id"), team.get("name")),
                "Year":  year,
                "POS":   position.get("abbreviation"),
                "Age":   stat.get("age"),
                "G":     stat.get("gamesPlayed"),
                "GS":    stat.get("gamesStarted"),
                "Inn":   stat.get("innings"),
                "PO":    stat.get("putOuts"),
                "A":     stat.get("assists"),
                "E":     stat.get("errors"),
                "DP":    stat.get("doublePlays"),
                "FP":    stat.get("fielding"),
                "RF9":   stat.get("rangeFactorPer9Inn"),
                "RFG":   stat.get("rangeFactorPerGame"),
            })
        time.sleep(SLEEP_SEC)
        print(f"{len(splits)} rows")

    df = pd.DataFrame(rows)
    print(f"  Total: {len(df)} fielder-position-season rows")
    return df


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    errors = []

    print("Loading team abbreviations...")
    team_abbr = load_team_abbreviations()
    print(f"  {len(team_abbr)} teams loaded\n")

    print(f"Fetching pitching stats {START_YEAR}–{END_YEAR} from MLB Stats API...")
    try:
        pitching_df = scrape_pitching(team_abbr)
        pitching_df.to_csv("pitching.csv", index=False)
        print("  Saved → pitching.csv\n")
    except Exception as e:
        print(f"\n  SKIPPED pitching.csv: {e}\n")
        errors.append("pitching")

    print(f"Fetching fielding stats {START_YEAR}–{END_YEAR} from MLB Stats API...")
    try:
        fielding_df = scrape_fielding(team_abbr)
        fielding_df.to_csv("fielding.csv", index=False)
        print("  Saved → fielding.csv\n")
    except Exception as e:
        print(f"\n  SKIPPED fielding.csv: {e}\n")
        errors.append("fielding")

    if not errors:
        print("Done! Both files saved.")
        print("Next step:  python3 ingest_data.py")
    else:
        print(f"Completed with errors in: {', '.join(errors)}")


if __name__ == "__main__":
    main()
