import os
import json
import csv
from collections import defaultdict
from datetime import datetime


def Test_MatchWise(json_dir, output_csv, start_date, end_date):
    """
    Processes all JSON files in the given directory for Test/MDM matches and saves the results to a CSV file.
    Only includes matches within the specified date range (start_date to end_date).

    Args:
        json_dir (str): Path to the directory containing the JSON files with match data.
        output_csv (str): Path to the output CSV file where the processed data will be saved.
        start_date (str): Start date (inclusive) in the format 'YYYY-MM-DD' to filter matches.
        end_date (str): End date (inclusive) in the format 'YYYY-MM-DD' to filter matches.

    Returns:
        None: The function processes the JSON data and writes the results to the specified CSV file.
    """
    
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_csv)
    os.makedirs(output_dir, exist_ok=True)

    # Convert start_date and end_date from string to datetime objects
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None

    # List of fields for CSV
    csv_fields = [
        'match_id', 'player_id', 'player_name', 'team_name', 'runs_scored', 'balls_faced', 'no_of_fours', 'no_of_sixes',
        'no_of_catches', 'runouts', 'balls_bowled', 'dot_balls',
        'wickets', 'LBWs/Bowled', 'runs_conceded', 'stumpings', 'date', 'venue', 'match_type', 'gender'
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

            # Extract match date
            match_date = match_data['info']['dates'][0]
            match_date_obj = datetime.strptime(match_date, "%Y-%m-%d")  # Convert to datetime object

            # Check if match is within the specified date range
            # if (start_date_obj and match_date_obj < start_date_obj) or (end_date_obj and match_date_obj > end_date_obj):
            #     continue  # Skip this match if it's outside the date range

            if (match_date_obj < start_date_obj) or (match_date_obj > end_date_obj):
                continue  # Skip this match if it's outside the date range

            # Check if match type is "Test" or "MDM"
            match_type = match_data['info']['match_type']
            if match_type.lower() in ['test', 'mdm']:

                # Extract match details
                venue = match_data['info'].get('city', "Unknown Venue")

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
                    'date': match_date,
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
                            bowler = delivery['bowler']

                            # Handle extras
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


if __name__ == "__main__":

    # Define the date range
    start_date = datetime.strptime("2000-01-01", "%Y-%m-%d")  # Start date (adjust as needed)
    end_date = datetime.strptime("2024-12-31", "%Y-%m-%d")  # End date (adjust as needed)
    
    # Specify the JSON directory, output CSV file, and date constraints
    json_dir='../data/raw/cricksheet_data/all_json'
    output_csv='../data/interim/Test_MatchWise.csv'
  
    Test_MatchWise(json_dir, output_csv, start_date, end_date)
