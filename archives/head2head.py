import json
import csv
import os

# Define the JSON file and output CSV file
json_file = "E:/CODING/Dream-11/tests_json/64012.json"  # Replace this with the name of your JSON file
output_csv = "batsman_vs_bowler_data_64012.csv"

# List of fields for CSV
csv_fields = [
    'match_id','batsman_id', 'batsman_name', 'bowler_id', 'bowler_name',
    'runs_scored', 'balls_faced','runs_conceded','balls_bowled', '4s', '6s', 'wickets',
    'gender', 'venue', 'date', 'match_type','wicket_type_1','wicket_type_2'
]

# Load JSON data
with open(json_file, "r") as f:
    match_data = json.load(f)

# Extract match type and skip if it's a Test match
match_type = match_data['info']['match_type']
if match_type.lower() == "testa":
    print("Skipping Test match.")
else:
    # Extract match details
    match_date = match_data['info']['dates'][0]
    venue = match_data['info']['venue']
    gender = match_data['info']['gender']
    match_id = os.path.basename(json_file).replace('.json', '')

    # Map player names to their IDs from the registry
    player_registry = match_data['info']['registry']['people']

    # Dictionary to store aggregated stats for each batsman-bowler pair
    head_to_head_data = {}

    # Iterate through each inning in the match
    i=0
    for inning in match_data['innings']:
        i=i+1
        if 'overs' not in inning:
            continue  # Skip this inning or handle it accordingly

        for over in inning['overs']:
            for delivery in over['deliveries']:
                # Extract delivery details
                batter = delivery['batter']
                bowler = delivery['bowler']
                
                
                # Generate unique key for batsman-bowler pair
                key = (batter, bowler)

                # Update the aggregated stats
                if key not in head_to_head_data:
                    head_to_head_data[key] = {
                
                        'batsman_id': player_registry[batter],
                        'batsman_name': batter,
                        'bowler_id': player_registry[bowler],
                        'bowler_name': bowler,
                        'runs_scored': 0,
                        'balls_faced': 0,
                        'runs_conceded': 0,
                        'balls_bowled': 0,
                        '4s': 0,
                        '6s': 0,
                        'wickets': 0,
                        'wicket_type_1':"",
                        'wicket_type_2':""

                        
                    }

                #Handle extras
                extras = delivery.get('extras', {}) 
                # runs_scored = delivery['runs']['batter']
                # total_runs = delivery['runs']['total']
                # fours = 1 if runs == 4 else 0
                # sixes = 1 if runs == 6 else 0


                if 'byes' in extras:
                    head_to_head_data[key]['balls_bowled'] += 1
                    head_to_head_data[key]['balls_faced']+=1
                    head_to_head_data[key]['runs_conceded']+=extras['byes']
                elif 'legbyes' in extras:
                    head_to_head_data[key]['balls_bowled'] += 1
                    head_to_head_data[key]['balls_faced']+=1
                    head_to_head_data[key]['runs_conceded']+=extras['legbyes']  
                elif 'wides' in extras:
                     head_to_head_data[key]['runs_conceded'] += extras['wides']
                     head_to_head_data[key]['balls_bowled']+=1
                elif 'noballs' in extras:
                    head_to_head_data[key]['runs_conceded'] += extras['noballs'] + delivery['runs']['batter']
                    head_to_head_data[key]['runs_scored'] += delivery['runs']['batter']
                    head_to_head_data[key]['balls_faced'] += 1
                    if delivery['runs']['batter'] == 4:
                        head_to_head_data[key]['4s'] += 1
                    elif delivery['runs']['batter'] == 6:
                        head_to_head_data[batter]['6s'] += 1
                else:
                    head_to_head_data[key]['balls_bowled'] += 1
                    head_to_head_data[key]['balls_faced'] += 1
                    head_to_head_data[key]['runs_conceded'] += delivery['runs']['total']
                    head_to_head_data[key]['runs_scored'] += delivery['runs']['total']
                    if delivery['runs']['batter'] == 4:
                        head_to_head_data[key]['4s'] += 1
                    elif delivery['runs']['batter'] == 6:
                        head_to_head_data[key]['6s'] += 1

                # Initialize wicket-related details
                
                if 'wickets' in delivery:
                    for wicket_info in delivery['wickets']:
                        if wicket_info['player_out'] == batter:
                            head_to_head_data[key]['wickets'] += 1   # Wicket taken :
                            if i==1 or i==2:
                                head_to_head_data[key]['wicket_type_1']=wicket_info['kind']
                            elif i==3 or i==4 :
                                head_to_head_data[key]['wicket_type_2']=wicket_info['kind']


    # Write aggregated data to the CSV
    with open(output_csv, mode="w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_fields)
        writer.writeheader()

        for key, stats in head_to_head_data.items():
            stats.update({
                'match_id': match_id,
                'gender': gender,
                'venue': venue,
                'date': match_date,
                'match_type': match_type
            })
            writer.writerow(stats)

    print(f"Head-to-head data saved to {output_csv}")
