from ODI import *
from Test import *
from T20 import *
from venue import *
"""
Cricket Match Data Processing

This script processes cricket match data for ODI, Test, and T20 formats to compute various statistics for each player. 
It outputs three types of statistics:
1. Career Statistics: Aggregate stats for each player.
2. Recent Performance: Stats calculated over a sliding window of the last 5 matches.
3. Venue-based Performance: Stats specific to each player-venue combination.

The script reads match data from CSV files and computes the following player performance metrics:
- Batting: Total runs, 100s, 50s, sixes, fours, average runs, strike rate.
- Bowling: Wickets, bowling average, economy rate.
- Fielding: Catches, runouts.

The data is saved into new CSV files, one for each category (Career, Recent, Venue) and for each match format (ODI, Test, T20).
"""

# ----------------ODI--------------------------------------------
# Call the function with the appropriate file paths
input_file = '../data/interim/ODI_MatchWise_fantasy_points.csv'
output_file = '../data/processed/ODI/career_odi.csv'
career_ODI(input_file, output_file)

input_file = '../data/interim/ODI_MatchWise_fantasy_points.csv'
output_file = '../data/processed/ODI/recent_odi.csv'
recent_ODI(input_file, output_file)

input_file = '../data/interim/ODI_MatchWise_fantasy_points.csv'
output_file = '../data/processed/ODI/venue_odi.csv'
venue_ODI(input_file, output_file)


# ----------------Test-------------------------------------------

input_file = '../data/interim/Test_MatchWise_fantasy_points.csv'
output_file = '../data/processed/Test/career_test.csv'
career_Test(input_file, output_file)

input_file = '../data/interim/Test_MatchWise_fantasy_points.csv'
output_file = '../data/processed/Test/recent_test.csv'
recent_Test(input_file, output_file)

input_file = '../data/interim/Test_MatchWise_fantasy_points.csv'
output_file = '../data/processed/Test/venue_test.csv'
venue_Test(input_file, output_file)


# ----------------T20--------------------------------------------
input_file = '../data/interim/T20_MatchWise_fantasy_points.csv'
output_file = '../data/processed/T20/career_t20.csv'
career_T20(input_file, output_file)

input_file = '../data/interim/T20_MatchWise_fantasy_points.csv'
output_file = '../data/processed/T20/recent_t20.csv'
recent_T20(input_file, output_file)

input_file = '../data/interim/T20_MatchWise_fantasy_points.csv'
output_file = '../data/processed/T20/venue_t20.csv'
venue_T20(input_file, output_file)


# ----------------venues--------------------------------------------
get_venues()