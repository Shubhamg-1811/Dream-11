import os
import json
import csv
from collections import defaultdict
from datetime import datetime


def T20_MatchWise(json_dir, output_csv, start_date=None, end_date=None):
    """
    Processes T20 match data from JSON files in the given directory and writes player statistics to a CSV file.

    The function extracts match and player performance data from T20 JSON match files, filters the data by the 
    specified date range (if provided), and saves the processed information into a CSV file. Player statistics include 
    runs, wickets, boundaries, and other relevant metrics.

    Args:
        json_dir (str): Directory containing the T20 JSON match files.
        output_csv (str): Path to the output CSV file where the processed data is saved.
        start_date (str, optional): Start date (in YYYY-MM-DD format) to filter matches. Defaults to None.
        end_date (str, optional): End date (in YYYY-MM-DD format) to filter matches. Defaults to None.

    Returns:
        None: The function writes the results to the specified CSV file.
    """
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_csv)
    os.makedirs(output_dir, exist_ok=True)

    # List of fields for CSV
    csv_fields = [
        'match_id', 'player_id', 'player_name', 'team_name', 'runs_scored', 'balls_faced', 'no_of_fours', 'no_of_sixes',
        'no_of_catches', 'runouts', 'balls_bowled', 'dot_balls',
        'wickets', 'LBWs/Bowled', 'runs_conceded', 'stumpings', 'out', 'date', 'venue', 'match_type', 'gender'
    ]

    # Initialize the CSV writer
    with open(output_csv, mode="w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_fields)
        writer.writeheader()

        # Loop through all files in the directory
        for file_name in os.listdir(json_dir):
            if not file_name.endswith(".json"):  # Process only JSON files
                continue

            file_path = os.path.join(json_dir, file_name)

            # Load JSON data
            with open(file_path, "r") as f:
                match_data = json.load(f)

            # Check if match type is "T20" or "IT20"
            match_type = match_data['info']['match_type']

            if match_type.lower() in ['t20', 'it20']:
                # Extract match details
                match_date_str = match_data['info']['dates'][0]
                match_date = datetime.strptime(match_date_str, "%Y-%m-%d")
                venue = match_data['info'].get('city', "Unknown Venue")

                # Filter matches based on the given date range
                if start_date and match_date < datetime.strptime(start_date, "%Y-%m-%d"):
                    continue
                if end_date and match_date > datetime.strptime(end_date, "%Y-%m-%d"):
                    continue

                # Initialize dictionary to store player statistics
                player_stats = defaultdict(lambda: {
                    'match_id': file_name.split('.')[0],
                    'player_id': None,
                    'team_name': None,
                    'runs_scored': 0,
                    'balls_faced': 0,
                    'no_of_fours': 0,
                    'no_of_sixes': 0,
                    'no_of_catches': 0,
                    'runouts': 0,
                    'balls_bowled': 0,
                    'dot_balls': 0,
                    'wickets': 0,
                    'LBWs/Bowled': 0,
                    'runs_conceded': 0,
                    'stumpings': 0,
                    'out': "DNB",  # Did not bat
                    'date': match_date_str,
                    'venue': venue,
                    'match_type': match_type,
                    'gender': match_data['info']['gender'],
                })

                # Map player names to their IDs from the registry
                player_registry = match_data['info']['registry']['people']

                # Assign player IDs to their statistics
                for player_name, player_id in player_registry.items():
                    player_stats[player_name]['player_id'] = str(player_id)

                # Assign team names to players
                if 'players' in match_data['info']:
                    for team_name, team_players in match_data['info']['players'].items():
                        for player_name in team_players:
                            if player_name in player_stats:
                                player_stats[player_name]['team_name'] = team_name

                # Iterate through each inning in the match
                for inning in match_data['innings']:
                    if 'overs' not in inning:
                        continue  # Skip this inning or handle it accordingly

                    for over in inning['overs']:
                        for delivery in over['deliveries']:
                            # Extract batter, non-striker, and bowler information
                            batter = delivery['batter']
                            non_striker = delivery['non_striker']
                            bowler = delivery['bowler']

                            # Update stats for batter and non-striker
                            if player_stats[batter]['out'] == 'DNB':
                                player_stats[batter]['out'] = 'not out'
                            if player_stats[non_striker]['out'] == 'DNB':
                                player_stats[non_striker]['out'] = 'not out'

                            # Handle extras and update stats
                            extras = delivery.get('extras', {})
                            if 'byes' in extras or 'legbyes' in extras:
                                player_stats[bowler]['balls_bowled'] += 1
                            elif 'wides' in extras:
                                player_stats[bowler]['runs_conceded'] += extras['wides']
                            elif 'noballs' in extras:
                                player_stats[bowler]['runs_conceded'] += extras['noballs'] + delivery['runs']['batter']
                                player_stats[batter]['runs_scored'] += delivery['runs']['batter']
                                player_stats[batter]['balls_faced'] += 1
                                if delivery['runs']['batter'] == 4:
                                    player_stats[batter]['no_of_fours'] += 1
                                elif delivery['runs']['batter'] == 6:
                                    player_stats[batter]['no_of_sixes'] += 1
                            else:
                                player_stats[bowler]['balls_bowled'] += 1
                                player_stats[bowler]['runs_conceded'] += delivery['runs']['total']
                                if delivery['runs']['total'] == 0:
                                    player_stats[bowler]['dot_balls'] += 1

                            # Update batter's stats
                            if 'byes' not in extras and 'legbyes' not in extras and 'wides' not in extras and 'noballs' not in extras:
                                runs_scored = delivery['runs']['batter']
                                player_stats[batter]['runs_scored'] += runs_scored
                                player_stats[batter]['balls_faced'] += 1
                                if runs_scored == 4:
                                    player_stats[batter]['no_of_fours'] += 1
                                elif runs_scored == 6:
                                    player_stats[batter]['no_of_sixes'] += 1
                            elif 'byes' in extras or 'legbyes' in extras:
                                player_stats[batter]['balls_faced'] += 1

                            # Handle wickets
                            if 'wickets' in delivery:
                                for wicket_info in delivery['wickets']:
                                    player_out = wicket_info['player_out']

                                    # Update out status for dismissed players
                                    if player_out in [batter, non_striker]:
                                        player_stats[player_out]['out'] = "out"

                                    if wicket_info['kind'] == 'caught':
                                        player_stats[bowler]['wickets'] += 1
                                        fielder = wicket_info.get('fielders', [{}])[0].get('name', None)
                                        if fielder:
                                            player_stats[fielder]['no_of_catches'] += 1
                                    elif wicket_info['kind'] == 'run out':
                                        for fielder_info in wicket_info.get('fielders', []):
                                            fielder_name = fielder_info.get('name', None)
                                            if fielder_name:
                                                player_stats[fielder_name]['runouts'] += 1
                                    elif wicket_info['kind'] == 'stumped':
                                        player_stats[bowler]['wickets'] += 1
                                        stumper = wicket_info.get('fielders', [{}])[0].get('name', None)
                                        if stumper:
                                            player_stats[stumper]['stumpings'] += 1
                                    elif wicket_info['kind'] in ['bowled', 'lbw']:
                                        player_stats[bowler]['LBWs/Bowled'] += 1
                                        player_stats[bowler]['wickets'] += 1
                                    else:
                                        player_stats[bowler]['wickets'] += 1

                # Write player stats to CSV
                for player, stats in player_stats.items():
                    stats_row = {'player_name': player}
                    stats_row.update(stats)
                    writer.writerow(stats_row)

    print(f"Data saved to {output_csv}")


# Example usage:
if __name__ == "__main__":
    json_dir='../data/raw/cricksheet_data/all_json'
    output_csv='../data/interim/T20_MatchWise.csv'
    start_date = "2000-01-01"
    end_date = "2024-12-01"

    T20_MatchWise(json_dir, output_csv, start_date, end_date)
