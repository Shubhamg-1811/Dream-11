import pandas as pd
import os


def get_venues():
    format = "Overall"
    file = os.path.join(os.path.dirname(__file__), f"../data/interim/{format}_MatchWise_fantasy_points.csv")


    # Load the necessary dataset
    df = pd.read_csv(file, low_memory=False)

    # Extract unique venues
    unique_venues = df['venue'].drop_duplicates()

    # Convert to a DataFrame
    unique_venues_df = pd.DataFrame(unique_venues)

    # Save the unique venues to a CSV file
    output_file = os.path.join(os.path.dirname(__file__), f"../data/interim/venues.csv")
    unique_venues_df.to_csv(output_file, index=False, header=['venue'])

    # print(f"CSV file '{output_file}' containing unique venues created successfully!")

    unique_venues_df.to_csv('CSVs/Final/venues.csv', index=False)
    # print(unique_venues_df)