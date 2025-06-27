import os
import json
import csv
from collections import defaultdict

# Define the directory containing JSON files
json_dir = "./all_json"
overall_output_csv = "./CSVs/Overall_PlayerStats.csv"

# Ensure the output directory exists
output_dir = os.path.dirname(overall_output_csv)
os.makedirs(output_dir, exist_ok=True)

# Fields for the overall stats CSV
overall_csv_fields = [
    'player_id', 'player_name', 'batting_innings', 'bowling_innings',
    'total_runs_scored', 'total_balls_faced', 'total_fours', 'total_sixes',
    'total_catches', 'total_runouts', 'total_balls_bowled', 'total_dot_balls',
    'total_wickets', 'total_LBWs/Bowled', 'total_runs_conceded', 'total_stumpings'
]

# Initialize dictionary for overall stats
overall_stats = defaultdict(lambda: {
    'batting_innings': 0,
    'bowling_innings': 0,
    'total_runs_scored': 0,
    'total_balls_faced': 0,
    'total_fours': 0,
    'total_sixes': 0,
    'total_catches': 0,
    'total_runouts': 0,
    'total_balls_bowled': 0,
    'total_dot_balls': 0,
    'total_wickets': 0,
    'total_LBWs/Bowled': 0,
    'total_runs_conceded': 0,
    'total_stumpings': 0
})

# Loop through all JSON files
for file_name in os.listdir(json_dir):
    if not file_name.endswith(".json"):  # Skip non-JSON files
        continue

    file_path = os.path.join(json_dir, file_name)

    # Load JSON data
    with open(file_path, "r") as f:
        try:
            match_data = json.load(f)
        except json.JSONDecodeError:
            continue

    # Map player names to their IDs
    player_registry = match_data['info']['registry']['people']

    # Process each inning
    for inning in match_data.get('innings', []):
        batter_participation = set()  # Tracks batters who participated in this inning
        bowler_participation = set()  # Tracks bowlers who participated in this inning

        for over in inning.get('overs', []):
            for delivery in over.get('deliveries', []):
                batter = delivery['batter']
                bowler = delivery['bowler']

                # Track batting innings
                if batter not in batter_participation:
                    batter_participation.add(batter)
                    overall_stats[batter]['batting_innings'] += 1
                    overall_stats[batter]['player_id'] = str(player_registry.get(batter, "Unknown"))
                    overall_stats[batter]['player_name'] = batter

                # Update batter stats
                batter_stats = overall_stats[batter]
                batter_stats['total_runs_scored'] += delivery.get('runs', {}).get('batter', 0)
                batter_stats['total_balls_faced'] += 1
                batter_stats['total_fours'] += 1 if delivery.get('runs', {}).get('batter', 0) == 4 else 0
                batter_stats['total_sixes'] += 1 if delivery.get('runs', {}).get('batter', 0) == 6 else 0

                # Track bowling innings
                if bowler not in bowler_participation:
                    bowler_participation.add(bowler)
                    overall_stats[bowler]['bowling_innings'] += 1
                    overall_stats[bowler]['player_id'] = str(player_registry.get(bowler, "Unknown"))
                    overall_stats[bowler]['player_name'] = bowler

                # Update bowler stats
                bowler_stats = overall_stats[bowler]
                bowler_stats['total_balls_bowled'] += 1
                bowler_stats['total_runs_conceded'] += delivery.get('runs', {}).get('total', 0)
                bowler_stats['total_dot_balls'] += 1 if delivery.get('runs', {}).get('total', 0) == 0 else 0

                if 'wickets' in delivery:
                    bowler_stats['total_wickets'] += len(delivery['wickets'])
                    bowler_stats['total_LBWs/Bowled'] += sum(
                        1 for wicket in delivery['wickets'] if wicket.get('kind') in ['bowled', 'lbw']
                    )

                    for wicket in delivery['wickets']:
                        # Track fielders
                        for fielder_info in wicket.get('fielders', []):
                            fielder_name = fielder_info.get('name')
                            if fielder_name:
                                overall_stats[fielder_name]['player_id'] = str(player_registry.get(fielder_name, "Unknown"))
                                overall_stats[fielder_name]['player_name'] = fielder_name
                                fielder_stats = overall_stats[fielder_name]

                                if wicket.get('kind') == 'caught':
                                    fielder_stats['total_catches'] += 1
                                elif wicket.get('kind') == 'run out':
                                    fielder_stats['total_runouts'] += 1
                                elif wicket.get('kind') == 'stumped':
                                    fielder_stats['total_stumpings'] += 1

# Write overall stats to a single CSV
with open(overall_output_csv, mode="w", newline="") as overall_csv:
    writer = csv.DictWriter(overall_csv, fieldnames=overall_csv_fields)
    writer.writeheader()
    for player_name, stats in overall_stats.items():
        stats_row = {'player_name': player_name, **stats}
        writer.writerow(stats_row)

print(f"Overall stats written to {overall_output_csv}")
