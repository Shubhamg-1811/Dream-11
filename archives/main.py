# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

# Run the following command to run the backend locally!
# uvicorn main:app --reload --port 8000

DEBUG = True


def date_(date: str):
    x = date.split('-')[::-1]
    return ' / '.join(i for i in x)
# -------------------------------------------------------------------------------------------------


def calculate_dream_team(players, match_group):
    try:
        # Step 1: Pick one player from each role
        selected_players = []
        for role in ["Batsman", "Bowler", "Wicket-Keeper", "All-Rounder"]:
            role_players = [p for p in players if p["role"] == role]
            if role_players:
                selected_players.append(
                    max(role_players, key=lambda x: x["fantasy_points"]))

        # Step 2: Select remaining players to make a team of 11
        remaining_players = [p for p in players if p not in selected_players]
        remaining_players.sort(key=lambda x: x["fantasy_points"], reverse=True)

        while len(selected_players) < 11:
            next_player = remaining_players.pop(0)
            selected_players.append(next_player)

        # Step 3: Ensure team diversity
        team_counts = pd.DataFrame(selected_players)[
            "team_name"].value_counts()
        if team_counts.max() == 11:
            # Replace the lowest fantasy point player with the highest fantasy point player
            # from the other team
            other_team = [team for team in match_group["team_name"].unique()
                          if team not in team_counts.index][0]
            lowest_fantasy_player = min(
                selected_players, key=lambda x: x["fantasy_points"])
            replacement_player = max(
                [p for p in players if p["team_name"] ==
                    other_team and p not in selected_players],
                key=lambda x: x["fantasy_points"]
            )
            selected_players.remove(lowest_fantasy_player)
            selected_players.append(replacement_player)

        # Step 4: Assign Captain and Vice-captain
        selected_players.sort(key=lambda x: x["fantasy_points"], reverse=True)

        # captain = selected_players[0]
        # vice_captain = selected_players[1]
        # Adjust fantasy points for captain and vice-captain
        # for player in selected_players:
        #     if player == captain:
        #         player["fantasy_points"] *= 2
        #     elif player == vice_captain:
        #         player["fantasy_points"] *= 1.5

        return selected_players, "Optimal"

    except Exception as e:
        print(f"Error in calculating dream team: {e}")
        return None, "Error"
# --------------------------------------------------------------------------------------------------


app = FastAPI()

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    # Update this if your frontend is served elsewhere
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/recommended_team")
def get_recommended_team(data: dict):
    # Extract data from the request
    team1 = data.get('team1')
    team2 = data.get('team2')
    players_team1 = data.get('playersTeam1')
    players_team2 = data.get('playersTeam2')
    match_date = data.get('matchDate')
    tournament_type = data.get('tournamentType')
    if DEBUG:
        print("Recommend Team:")
        print(f"    team1: {team1}")
        print(f"    team2: {team2}")
        print(f"    players_team1: {players_team1}")
        print(f"    players_team2: {players_team2}")
        print(f"    match_date: {match_date}")
        print(f"    tournament_type: {tournament_type}")

    # Validate data
    if not all([team1, team2, players_team1, players_team2, match_date, tournament_type]):
        raise HTTPException(status_code=400, detail="Invalid input data.")

    # Generate recommended team using ML model
    recommended_team = generate_mock_team(players_team1 + players_team2)

    return {"recommended_team": recommended_team}


def generate_mock_team(players):
    # Mock implementation
    import random
    recommended_team = []
    for player in random.sample(players, 11):
        recommended_team.append({
            "name": player,
            "photo": "",  # Placeholder for player photo URL
            "role": random.choice(["Batsman", "Bowler", "All-rounder", "Wicketkeeper"]),
            "predicted_points": round(random.uniform(20, 100), 1),
            "justification": "Player selected based on performance metrics.",
            "isCaptain": False,
            "isViceCaptain": False,
            "team": "",  # Team name can be assigned appropriately
        })

    recommended_team.sort(
        key=lambda player: player["predicted_points"], reverse=True)

    # Assign Captain and Vice-Captain
    if recommended_team:
        recommended_team[0]["isCaptain"] = True
    if len(recommended_team) > 1:
        recommended_team[1]["isViceCaptain"] = True

    return recommended_team

# Additional endpoints for model analysis


@app.post("/api/analyze_model")
def analyze_model(data: dict):
    # Extract date ranges
    training_start = data.get('training_start')
    training_end = data.get('training_end')
    testing_start = data.get('testing_start')
    testing_end = data.get('testing_end')
    # Validate dates
    if not all([training_start, training_end, testing_start, testing_end]):
        raise HTTPException(status_code=400, detail="Invalid date ranges.")
    if training_start >= training_end:
        raise HTTPException(
            status_code=400, detail="Training date ranges are invalid!")
    if testing_start >= testing_end:
        raise HTTPException(
            status_code=400, detail="Testing date ranges are invalid!")

    if DEBUG:

        print("Model Analysis:")
        print(f"    training_start  : {date_(training_start)}")
        print(f"    training_end    : {date_(training_end)}")
        print(f"    testing_start   : {date_(testing_start)}")
        print(f"    testing_end     : {date_(testing_end)}")

    # Reduce the datraframe for training data and train the model
    # Perf. metrics

    # Placeholder: Analyze model performance

    performance_metrics = {
        "accuracy": 0.85,
        "precision": 0.80,
        "recall": 0.78,
        "f1_score": 0.79,
    }

    return performance_metrics


@app.get("/api/download_model")
def download_model():
    # Placeholder: Return model file
    # In production, you'd return the actual model file
    raise HTTPException(
        status_code=501, detail="Download model not implemented.")


@app.post("/api/retrain_model")
def retrain_model():
    # Placeholder: Retrain the ML model
    # In production, you'd kick off a retraining process

    # load data
    # preprocess data
    # train model

    return {"detail": "Model retraining initiated."}


@app.post("/api/detect_tournament_type")
def choose_model(data: dict):
    tournamentType = data.get('tournamentType')
    if DEBUG:
        print(f"tournamentType: {tournamentType}")

    if tournamentType == "T20":
        # load T20 model    |   model.load("model_artifacts/model_T20_upto_30Jun2024.pkl")
        ...
    elif tournamentType == "ODI":
        # load ODI model    |   model.load("model_artifacts/model_ODI_upto_30Jun2024.pkl")
        ...
    else:
        # load Test model   |   model.load("model_artifacts/model_Test_upto_30Jun2024.pkl")
        ...


@app.post("/api/detect_date")
def detect_date(data: dict):
    matchDate = data.get('matchDate')
    if DEBUG:
        print(f"matchDate: {date_(matchDate)}")

    if matchDate <= '2001-01-01':
        raise HTTPException(
            status_code=400, detail="Accessed date before 1st January, 2001")

    return {"detail": "Accessed date before 1st January, 2001"}


@app.get("/api/players")
def get_players():
    """
    API to get ID-player-designation data from a CSV file.
    """
    try:
        # Load the CSV file containing player data
        player_data = pd.read_csv("../../CSVs/Designation.csv")

        # Convert the data to a JSON format
        players = player_data.to_dict(orient="records")
        return {"players": players}
    except Exception as e:
        return {"error": str(e)}
