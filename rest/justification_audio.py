from gtts import gTTS
# from pprint import pprint
# TODO: IMPLEMENTATION INCOMPLETE
def generate_justification(player, tournament_type) -> str:
    """
    Args: 
        player (Dict[str, Union[str, list[float64]]]): player dictionary for whom the justification of his/her selection has to be generated
        tournament_type (str): type of the tournament (ODI, T20 or Test)
    Returns:
        str: justification as to why this player has been chosen in the predicted dream team
    """

    justification = ""
    def shap_insight(value, low_msg: str, medium_msg: str, high_msg: str) -> str:
        if value <= 0:
            return low_msg
        elif value <= 10:
            return medium_msg
        else:
            return high_msg

    # Extract player details
    player_name = player["player_name"]
    role = player["role"]
    shap_values = player["shap_values"]
    career_list = player["career"]
    recent_list = player["recent_form"]
    venue_list = player["venue"]

    # Initialize justification components
    career = ""
    recent_form = ""
    venue = ""

    shap_career: float = shap_values[0]
    shap_recent_form: float = shap_values[1]
    shap_venue: float = shap_values[2]

    career = shap_insight(
        shap_career,
        "steady career performance",
        "notable career record",
        "exceptional career record"
    )
    recent_form = shap_insight(
        shap_recent_form,
        "decent recent form",
        "good recent form",
        "great recent form"
    )
    venue = shap_insight(
        shap_venue,
        "is adaptable to the venue",
        "has good suitability for the venue",
        "has outstanding fit for the venue"
    )

    main_list = venue_list
    if max(shap_career,shap_recent_form,shap_venue) == shap_career:
        main_list = career_list
    elif max(shap_career,shap_recent_form,shap_venue) == shap_recent_form:
        main_list = recent_list
    else:
        main_list = venue_list

    try:
        match tournament_type:
            case "ODI":
                average_runs = round(main_list[5], 1)
                strike_rate = round(main_list[6], 1)
                avg_runs_per_wicket = round(main_list[8], 1)
                economy_rate = round(main_list[9], 1)
                match role.lower():
                    case "batsman":
                        extra_stats = f" This player has an average of {average_runs} runs and a strike rate of {strike_rate}." 
                    case "bowler":
                        extra_stats = f" This player averages {avg_runs_per_wicket} runs per wicket and maintains an economy rate of {economy_rate}."
                    case "wicket-keeper":
                        extra_stats = (
                        f" This player has an average of {average_runs} runs. "
                        # f"In addition, this player has completed {round(main_list[11], 1)} stumpings."
                    )
                    case "all-rounder":
                        extra_stats = (
                        f" This player has an average of {average_runs} runs and a strike rate of {strike_rate}. "
                        f"Additionally, this player averages {avg_runs_per_wicket} wickets per match and maintains an economy rate of {economy_rate}."
                    )
                    case _:
                        extra_stats = ""

            case "T20":
                average_runs = round(main_list[6], 1)
                strike_rate = round(main_list[7], 1)
                avg_runs_per_wicket = round(main_list[9], 1)
                economy_rate = round(main_list[10], 1)

                match role.lower():
                    case "batsman":
                        extra_stats = f" This player has an average of {average_runs} runs and a strike rate of {strike_rate}."
                    case "bowler":
                        extra_stats = f" This player averages {avg_runs_per_wicket} runs per wicket and maintains an economy rate of {economy_rate}."
                    case "wicket-keeper":
                        extra_stats = (
                        f" This player has an average of {average_runs} runs. "
                        # f"In addition, this player has completed {round(main_list[11], 1)} stumpings."
                    )
                    case "all-rounder":
                        extra_stats = (
                        f" This player has an average of {average_runs} runs and a strike rate of {strike_rate}. "
                        f"Additionally, this player averages {avg_runs_per_wicket} runs per wickets and maintains an economy rate of {economy_rate}."
                    )
                    case _:
                        extra_stats = ""

            case "Test":
                average_runs = round(main_list[6], 1)
                strike_rate = round(main_list[7], 1)
                avg_runs_per_wicket = round(main_list[9], 1)

                match role.lower():
                    case "batsman":
                        extra_stats = f"This player has an average of {average_runs} runs."
                    case "bowler":
                        extra_stats = f"This player averages {avg_runs_per_wicket} runs per wicket."
                    case "wicket-keeper":
                        extra_stats = (
                        f"This player has an average of {average_runs} runs."
                        # f"In addition, this player has completed {round(main_list[11], 1)} stumpings."
                    )
                    case "all-rounder":
                        extra_stats = (
                        f"This player has an average of {average_runs} runs. "
                        f"Additionally, this player averages {avg_runs_per_wicket} runs per wickets."
                    )
                    case _:
                        extra_stats = ""
            
        justification = (
            f"{player_name} is a {role} with {career}, {recent_form}, and {venue}. "
            f"{extra_stats}"
        )

    except Exception as e:
        print(f"{main_list=}")
        print(f"{shap_values=}")
        print(f"Error while generating justification: [{role} {len(main_list)=}]", e)
    return justification


# Function to generate audio
def generate_audio(text, filename):
    tts = gTTS(text=text, lang="en")
    tts.save(filename)
    print(f"Audio saved to {filename}")
