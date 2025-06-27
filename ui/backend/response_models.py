from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import List


class Player(BaseModel):
    player_id: str
    player_name: str
    role: str
    team_name: str
    def __str__(self):
        return f"{self.player_name} ({self.role}) [{self.player_id}]"

class RecommendedTeamRequest(BaseModel):
    players_team1: List[Player] = Field(...,
                                       description="List of players in Team 1")
    players_team2: List[Player] = Field(...,
                                       description="List of players in Team 2")
    match_date: datetime = Field(...,
                                description="Date of the match in YYYY-MM-DD format")
    tournament_type: str = Field(...,
                                description="Type of tournament (e.g., T20, ODI, Test)")
    venue: str = Field(..., description="Venue of the match")

    need_justification: bool
    # for pretty printing while debugging
    def __str__(self):
        team1 = self.players_team1[0].team_name
        team2 = self.players_team2[0].team_name
        team1_players = ""
        team2_players = ""
        i = 1
        for player in self.players_team1:
            team1_players += f"\n    {f"{i}.".ljust(3)} {str(player)}"
            i += 1
        i = 1
        for player in self.players_team2:
            team2_players += f"\n    {f"{i}.".ljust(3)} {str(player)}"
            i += 1
        return (
            f"Recommended Team Request:\n"
            f"Match Date      : {self.match_date.strftime('%Y-%m-%d')}\n"
            f"Tournament Type : {self.tournament_type}\n"
            f"Venue           : {self.venue}\n\n"
            f"{team1} Players:{team1_players}\n\n"
            f"{team2} Players:{team2_players}"
        )

class PlayerResponse(BaseModel):
    name: str
    role: str
    predicted_points: float
    justification: str
    is_captain: bool
    is_vice_captain: bool
    team: str
    def __str__(self):
        return f"{self.name} ({self.role}, {self.team}){' [Captain]'if self.is_captain else ''}{' [Vice-Captain]' if self.is_vice_captain else ''}"

class RecommendedTeamResponse(BaseModel):
    recommended_team: List[PlayerResponse]
    def __str__(self):
        players = ""
        i = 1
        for player in self.recommended_team:
            players += f"\n    {f"{i}.".ljust(3)} {str(player)}"
            i += 1
        return(f"\nPredicted Dream Team:{players}")


class AnalyzeModelRequest(BaseModel):
    training_start: datetime = Field(...,
                                     description="Start date for training data")
    training_end: datetime = Field(...,
                                   description="End date for training data")
    testing_start: datetime = Field(...,
                                    description="Start date for testing data")
    testing_end: datetime = Field(..., description="End date for testing data")

    # @field_validator('training_end')
    # def training_end_after_start(cls, v, values):
    #     if 'training_start' in values and v <= values['training_start']:
    #         raise HTTPException(status_code=500,detail='training_end must be after training_start')
    #     return v

    # @field_validator('testing_end')
    # def testing_end_after_start(cls, v, values):
    #     if 'testing_start' in values and v <= values['testing_start']:
    #         raise HTTPException(status_code=500,detail='testing_end must be after testing_start')
    #     return v

# TODO: change IT!
class PerformanceMetrics(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1_score: float


class RetrainModelResponse(BaseModel):
    detail: str


class DetectTournamentTypeRequest(BaseModel):
    tournament_type: str = Field(...,
                                description="Type of tournament (e.g., T20, ODI, Test)")


class DetectDateRequest(BaseModel):
    match_date: datetime = Field(...,
                                description="Date of the match in YYYY-MM-DD format")
