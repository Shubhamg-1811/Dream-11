# backend/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
from datetime import datetime
import pandas as pd
import logging
import uvicorn
import os
import sys
import zipfile

sys.path.append(os.path.abspath('../../'))
from model.predict_model import generate_dream_team
from model.train_model import train_model_ui2
from response_models import *
from rest.justification_audio import generate_justification, generate_audio

# Initialize FastAPI app
app = FastAPI(
    title="Dream11 Team Prediction API",
    description="API for recommending Dream11 teams using ML models",
    version="1.0.0"
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001", # for backup purposes if previous ones don't work
        "http://localhost:3002", # for backup purposes if previous ones don't work
    ],  # Update this as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    # filename="logs.log",
    handlers=[
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)

#---------------------------------------------------------------------------------------------------
tournament_type = "T20"
TRAINING_START = datetime.now()
TRAINING_END = datetime.now()
TESTING_START = datetime.now()
TESTING_END = datetime.now()
FILES_RELATIVE_PATH = {}
#---------------------------------------------------------------------------------------------------

# Endpoint Implementations

# TODO: TESTING
@app.post("/api/recommended_team", response_model=RecommendedTeamResponse)
def get_recommended_team(request: RecommendedTeamRequest):
    """
    Generate a recommended Dream11 team based on the provided players and match details.

    Args:
        request (RecommendedTeamRequest): request from frontend

    Raises:
        HTTPException: 400 - if teams' names are same
        HTTPException: 400 - if there are less than 11 total players passed in the request by mistake
        HTTPException: 500 - if dream team could not be generated
        HTTPException: 500 - if any error occurs while generating dream team

    Returns:
        RecommendedTeamResponse: response for frontend containing the recommended team
    """
    logger.info("Received request for recommended team.")
    logger.debug(request)

    # Validate team names
    if request.players_team1[0].team_name == request.players_team2[0].team_name:
        raise HTTPException(
            status_code=400, detail="team1 and team2 must be different.")
    
    team1 = [{"player_name":player.player_name, "player_id":player.player_id, "team_name":player.team_name, "role":player.role} for player in request.players_team1]
    team2 = [{"player_name":player.player_name, "player_id":player.player_id, "team_name":player.team_name, "role":player.role} for player in request.players_team2]
    all_players = team1 + team2

    # Validate number of players
    if len(all_players) < 11:
        raise HTTPException(
            status_code=400, detail="At least 11 players are required to form a team.")

    try:
        recommended_team = generate_dream_team(all_players, request.match_date,request.venue, request.tournament_type, request.need_justification)
        logger.debug(f"recommended_team: {recommended_team}")
        if not recommended_team:
            logger.exception("Failed to generate recommended team!")
            raise HTTPException(
                status_code=500, detail="Failed to generate recommended team.")
        from pprint import pprint
        pprint(f"{recommended_team=}")
        # Transform the team into the response model
        response_team = [
            PlayerResponse(
                name=player.get("player_name", "Unknown"),
                role=player.get("role", "Unknown"),
                predicted_points=round(player.get("predicted_points", 0.0), 1),
                justification=generate_justification(player, tournament_type) if request.need_justification else "",
                is_captain=player.get("is_captain", False),
                is_vice_captain=player.get("is_vice_captain", False),
                team=player.get("team_name", "")
            )
            for player in recommended_team
        ]
        response = RecommendedTeamResponse(recommended_team=response_team)
        logger.info(response)
        return response

    except Exception as e:
        logger.error(f"Error in get_recommended_team: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error.")


# TODO: IMPLEMENTATION INCOMPLETE
@app.post("/api/analyze_model", response_model=PerformanceMetrics)
def analyze_model(request: AnalyzeModelRequest):
    """
    Analyze the ML model performance based on the provided date ranges.

    Args:
        request (RecommendedTeamRequest): request from frontend containing all the dates.

    Raises:
        HTTPException (400): if teams' names are same
        HTTPException (500): if any error occurs while generating dream team

    Returns:
        PerformanceMetrics: response for frontend containing the performance metrics
    """

    logger.info("Received request to analyze model.")
    logger.debug(f"AnalyzeModelRequest: {request}")
    logger.info(f"{request.training_start=}")
    logger.info(f"{request.training_end=}")
    logger.info(f"{request.testing_start=}")
    logger.info(f"{request.testing_end=}")

    # Reformat dates for logging
    training_start_formatted = request.training_start.strftime("%Y-%m-%d")
    training_end_formatted = request.training_end.strftime("%Y-%m-%d")
    testing_start_formatted = request.testing_start.strftime("%Y-%m-%d")
    testing_end_formatted = request.testing_end.strftime("%Y-%m-%d")

    TRAINING_START = training_start_formatted
    TRAINING_END = training_end_formatted
    TESTING_START = testing_start_formatted
    TESTING_END = testing_end_formatted
    
    logger.info(f"""Model Analysis:
                            training_start  : {training_start_formatted}
                            training_end    : {training_end_formatted}
                            testing_start   : {testing_start_formatted}
                            testing_end     : {testing_end_formatted}""")

    try:
        if TRAINING_START > TRAINING_END:
            raise HTTPException(status_code=400, detail="Invalid Date Range for Training Period.")
        if TESTING_START > TESTING_END:
            raise HTTPException(status_code=400, detail="Invalid Date Range for Testing Period.")

        files = train_model_ui2(TRAINING_START,TRAINING_END,TESTING_START,TESTING_END)
        FILES_RELATIVE_PATH["files"] = files

        # dummy data for now
        # For demonstration, return static performance metrics
        performance_metrics = PerformanceMetrics(
            accuracy=0.85,
            precision=0.80,
            recall=0.78,
            f1_score=0.79
        )

        logger.info(f"Performance Metrics: {performance_metrics}")

        return performance_metrics

    except Exception as e:
        logger.error(f"Error in analyze_model: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error.")
    finally:
        print(f"{FILES_RELATIVE_PATH["files"]=}")


@app.get("/api/download_model")
def download_model():
    """
    Download the ML model that we just trained along with the summary of dream teams for the matches during the testing period.

    Raises:
        HTTPException (404): if models cannot be found.
        HTTPException (500): if any error occurs while fetching the models and their summary

    Returns:
        FileResponse: 6 files (3 model.pkl files for each of the tournament types and 3 for their summary of dream teams)
    """

    logger.info("Received request to download model.")

    zf = zipfile.ZipFile("../../model_artifacts_ui2/models.zip", mode="w")
    compression = zipfile.ZIP_DEFLATED
    try:
        for file in FILES_RELATIVE_PATH["files"]:
            zf.write(os.path.join(os.path.dirname(__file__), file), file.split("/")[-1], compress_type=compression)
    except Exception as e:
        logger.error("Model file not found.")
        raise HTTPException(status_code=404, detail="Model file not found.")
    finally:
        zf.close()
    logger.info(f"Dowloading files: {FILES_RELATIVE_PATH["files"]}")
    try:
        from fastapi.responses import FileResponse
        return FileResponse(path="../../model_artifacts_ui2/models.zip", filename="models_with_results.zip", media_type='application/octet-stream')
    except Exception as e:
        logger.error(f"Error in download_model: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error.")


# TODO: IMPLEMENTATION INCOMPLETE
@app.post("/api/retrain_model", response_model=RetrainModelResponse)
def retrain_model():
    """
    Endpoint to initiate retraining of the ML model.

    Raises:
        HTTPException (500): if any error occurs while retraining the models

    Returns:
        RetrainModelResponse: response to let frontend know that the retraining process has started
    """
    logger.info("Received request to retrain model.")
    try:
        # Placeholder: Implement actual retraining logic
        # Example:
        # retrain_process = initiate_retraining()
        # retrain_process.start()

        # For demonstration, we'll just return a success message
        return RetrainModelResponse(detail="Model retraining initiated.")

    except Exception as e:
        logger.error(f"Error in retrain_model: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to initiate model retraining.")


@app.post("/api/detect_tournament_type")
def detect_tournament_type(request: DetectTournamentTypeRequest):
    """
    Endpoint to select the appropriate ML model based on tournament type.

    Args:
        request (DetectTournamentTypeRequest): request from frontend containing the tournament type of the match that we want to predict.

    Raises:
        HTTPException (400): if tournament type is different from 
        HTTPException (404): if any error occurs while generating dream team
        HTTPException (500): if any error occurs while generating dream team

    Returns:
        PerformanceMetrics: response for frontend containing the performance metrics
    """
    tournament_type = request.tournament_type
    logger.info(f"Received request to detect tournament type. Type = {tournament_type}")
    logger.debug(f"DetectTournamentTypeRequest: {tournament_type}")


    model_artifacts = {
        # "T20": "model_artifacts/model_T20.pkl",
        # "ODI": "model_artifacts/model_ODI.pkl",
        # "Test": "model_artifacts/model_Test.pkl"
        "T20": os.path.join(os.path.dirname(__file__), "../../model_artifacts/T20/model_t20_HBR.pkl"),
        "ODI": os.path.join(os.path.dirname(__file__), "../../model_artifacts/ODI/model_odi_HBR.pkl"),
        "Test": os.path.join(os.path.dirname(__file__), "../../model_artifacts/Test/model_test_HBR.pkl"),
    }

    if tournament_type not in model_artifacts:
        logger.error(f"Invalid tournament type: {tournament_type}")
        raise HTTPException(status_code=400, detail="Invalid tournament type. Choose from T20, ODI, or Test.")

    model_path = model_artifacts[tournament_type]

    if not os.path.exists(model_path):
        logger.error(f"Model for {tournament_type} not found.")
        raise HTTPException(status_code=404, detail=f"Model for {tournament_type} not found.")

    try:
        # ignore pylance warning here as we use the model later
        # MODEL = pickle.load(model_path)
        # Placeholder: Load and return model details or status
        # Example:
        # model = load_model(model_path)
        # return {"detail": f"{tournament_type} model loaded successfully."}

        return {
            "detail": f"{tournament_type} model selected successfully.",
        }

    except Exception as e:
        logger.error(f"Error in detect_tournament_type: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to load the specified model.")


@app.post("/api/detect_date")
async def detect_date(request: DetectDateRequest):
    """
    Endpoint to validate the match date.
    """
    logger.info("Received request to detect date.")
    logger.debug(f"DetectDateRequest: {request.match_date}")

    match_date = request.match_date

    cutoff_date = datetime(2001, 12, 19)

    if match_date <= cutoff_date:
        logger.warning(f"Accessed date before {cutoff_date.strftime('%Y-%m-%d')}")
        raise HTTPException(
            status_code=400, detail="Accessed date before 19th December, 2001.")

    return {"detail": "Valid match date."}


@app.get("/api/players", response_model=Dict[str, List[Dict[str, Any]]])
async def get_players():
    """
    API to get ID-player-designation data from a CSV file.

    Returns:
        Dict[str, Any]: dictionary containing all players that have played since 2001
    """
    logger.info("Received request to get players data.")
    csv_path = os.path.join(os.path.dirname(__file__),
                            "../../data/interim/Designation.csv")

    if not os.path.exists(csv_path):
        logger.error("Designation.csv file not found.")
        raise HTTPException(
            status_code=404, detail="Player data file not found.")

    try:
        player_data = pd.read_csv(csv_path)
        players = player_data.to_dict(orient="records")
        logger.info(f"Loaded {len(players)} players from CSV.")
        return {"players": players}
    except Exception as e:
        logger.error(f"Error in get_players: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to load player data.")


@app.get("/api/venues", response_model=Dict[str,List])
async def get_venues():
    logger.info("Received request to get venues data.")

    # Specify the CSV path correctly (absolute path in your case)
    csv_path = os.path.join(os.path.dirname(__file__), f"../../data/interim/venues.csv")

    # Check if the file exists first
    if not os.path.exists(csv_path):
        logger.error(f"venues.csv file not found at {csv_path}.")
        raise HTTPException(
            status_code=404, detail="Venue data file not found.")

    try:
        # Load the CSV into a pandas DataFrame
        venue_df = pd.read_csv(csv_path)

        # Check if the expected column exists (assuming 'venue' is the name of the column)
        if 'venue' not in venue_df.columns:
            logger.error("CSV does not contain 'venue' column.")
            raise HTTPException(
                status_code=500, detail="CSV does not contain the expected 'venue' column.")

        # Convert to list of dictionaries
        # Only get the 'venue' column, assuming you want to return just venue names
        venues = venue_df['venue'].tolist()

        logger.info(f"Loaded {len(venues)} venues from CSV.")

        return {"venues": venues}

    except Exception as e:
        logger.error(f"Error in get_venues: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to load venue data.")

# Run the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True, reload_dirs=[".","../../model"])
