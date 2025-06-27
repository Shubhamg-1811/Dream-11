import pandas as pd


def calculate_fantasy_points(player: pd.core.series.Series):
    """
    Calculates the fantasy points for a given player based on their performance in a match.

    Parameters:
        player (pd.core.series.Series): A pandas Series containing player performance data such as runs, wickets, boundaries, etc.

    Returns:
        float: The calculated fantasy points for the player based on the defined scoring rules.
    
    Scoring Breakdown:
    - Batting: Points for runs, boundaries, sixes, milestones (50, 100, 30 in T20), and a duck penalty (for limited-overs matches).
    - Bowling: Points for wickets, LBWs/Bowled wickets, and economy rate.
    - Fielding: Points for catches, stumpings, and run-outs.
    """
    points = 0

    # Batting Points
    points += player['runs_scored']  # 1 point per run
    points += player['no_of_fours']  # 1 point per boundary
    points += player['no_of_sixes'] * 2  # 2 points per six

    # Bonus for milestones
    if player['runs_scored'] >= 100:
        points += 16 
    elif player['runs_scored'] >= 50:
        points += 8 
    elif player['runs_scored'] >= 30 and player['match_type'] in ['T20', 'IT20']:
        points += 4

    # Calculate duck penalty (Ask Harsh and Sohit)
    if player['match_type'] not in ['Test', 'MDM']: 
        if player['runs_scored'] == 0 and player['out'] == 'out':
            if player['match_type'] in ['IT20', 'ODM', 'ODI', 'T20']:
                points -= 2  # Duck penalty for ODI and T20
    # ignoring duck penalty in test matches!

    # Strike Rate Bonus/Penalty (applicable in limited-overs matches)
    if player['match_type'] in ['IT20', 'ODM', 'ODI', 'T20'] and player['balls_faced'] >= 10:
        strike_rate = (player['runs_scored'] / player['balls_faced']) * 100
        if player['match_type'] in ['T20', 'IT20']:
            if strike_rate > 170:
                points += 6
            elif 150 < strike_rate <= 170:
                points += 4
            elif 130 < strike_rate <= 150:
                points += 2
            elif 60 <= strike_rate < 70:
                points -= 2
            elif 50 <= strike_rate < 60:
                points -= 4
            elif strike_rate < 50:
                points -= 6
        elif player['match_type'] in ['ODI', 'ODM']:
            if strike_rate > 140:
                points += 6
            elif 120 < strike_rate <= 140:
                points += 4
            elif 100 < strike_rate <= 120:
                points += 2
            elif 40 <= strike_rate < 50:
                points -= 2
            elif 30 <= strike_rate < 40:
                points -= 4
            elif strike_rate < 30:
                points -= 6

    # Bowling Points
    points += player['wickets'] * 25  # 25 points per wicket
    # points += player['maidens'] * 12  # 12 points per maiden over

    # Bonus for wicket types
    if 'LBWs/Bowled' in player:
        points += player['LBWs/Bowled'] * 8  # 8 points per LBW/Bowled wicket

    # Bonus for wicket hauls
    if player['wickets'] >= 5:
        points += 16
    elif player['wickets'] == 4:
        points += 8
    elif player['wickets'] == 3:
        points += 4

    # Economy Rate Bonus/Penalty (applicable in limited-overs matches)
    if player['match_type'] in ['IT20', 'ODM', 'ODI', 'T20'] and player['balls_bowled'] / 6 >= 2:
        economy_rate = player['runs_conceded'] / (player['balls_bowled'] / 6)
        if player['match_type'] in ['T20', 'IT20']:
            if economy_rate < 5:
                points += 6
            elif 5 <= economy_rate < 6:
                points += 4
            elif 6 <= economy_rate < 7:
                points += 2
            elif 10 <= economy_rate < 11:
                points -= 2
            elif 11 <= economy_rate < 12:
                points -= 4
            elif economy_rate >= 12:
                points -= 6
        elif player['match_type'] in ['ODI', 'ODI']:
            if economy_rate < 2.5:
                points += 6
            elif 2.5 <= economy_rate < 3.5:
                points += 4
            elif 3.5 <= economy_rate < 4.5:
                points += 2
            elif 7 <= economy_rate < 8:
                points -= 2
            elif 8 <= economy_rate < 9:
                points -= 4
            elif economy_rate >= 9:
                points -= 6

    # Fielding Points
    points += player['no_of_catches'] * 8  # 8 points per catch
    points += player['stumpings'] * 12  # 12 points per stumping
    # avg of (6 + 12) / 2 points per direct hit run-out and points per thrower/catcher run-out
    points += player['runouts'] * ((6 + 12) // 2)

    return points


def add_fantasy_points(input_file: str, output_file: str):
    # Load the data
    df = pd.read_csv(input_file)
    
    # Calculate fantasy points for each player
    df['fantasy_points'] = df.apply(calculate_fantasy_points, axis=1)
    
    # Sort the dataframe by 'date' and 'match_id' to ensure that matches with the same match_id are grouped together
    df = df.sort_values(by=['date', 'match_id'], ascending=[True, True])
    
    # Save the updated dataframe to the output file
    df.to_csv(output_file, index=False)


# if __name__ == "__main__":
#     input_file = '../data/interim/ODI_MatchWise.csv'
#     output_file = '../data/interim/ODI_MatchWise_fantasy_points.csv'

#     add_fantasy_points(input_file, output_file)