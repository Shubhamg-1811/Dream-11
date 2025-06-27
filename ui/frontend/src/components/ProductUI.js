import React, { useState, useEffect } from "react";
import AsyncSelect from "react-select/async";
import axios from "axios";
import PlayerCard from "./PlayerCard";
import "./ProductUI.css";

const API_URL = "http://localhost:8000";

function ProductUI() {
  const [team1, setTeam1] = useState("");
  const [team2, setTeam2] = useState("");
  const [matchDate, setMatchDate] = useState("");
  const [venue, setVenue] = useState("");
  const [tournamentType, setTournamentType] = useState("T20");
  const [playersTeam1, setPlayersTeam1] = useState(Array(11).fill(""));
  const [playersTeam2, setPlayersTeam2] = useState(Array(11).fill(""));
  const [allPlayers, setAllPlayers] = useState([]); // Store all player options
  const [allVenues, setAllVenues] = useState([]); // Store all player options
  const [recommendedTeam, setRecommendedTeam] = useState([]);
  const [loading1, setLoading1] = useState(false);
  const [loading2, setLoading2] = useState(false);
  const [error, setError] = useState(null);
  const [need_justification, setNeedJustification] = useState(false);
  const [dateError, setDateError] = useState(null); // For date validation error

  const fetchPlayers = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/players`);
      if (!response) {
        console.log("Could not fetch players!");
        console.log(`${API_URL}/api/players`);
        return;
      }
      const playerOptions = response.data.players.map((player) => ({
        id: player.player_id,
        value: player.player_id,
        label: `${player.player_name} (${player.role}) [ID: ${player.player_id}]`,
        role: player.role,
        name: player.player_name,
      }));
      setAllPlayers(playerOptions);
    } catch (err) {
      console.error("Error fetching players:", err);
    }
  };
  const fetchVenues = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/venues`);
      if (!response || !response.data || !response.data.venues) {
        console.log("No venues found!");
        return;
      }
      const venueOptions = response.data.venues.map((venue) => ({
        name: venue,
        label: venue,
        value: venue,
      }));
      setAllVenues(venueOptions);
    } catch (err) {
      console.error("Error fetching venues:", err);
      // Log the full error response
      if (err.response) {
        console.error("Error response:", err.response.data);
        alert("Error: " + err.response.data.detail); // Show the error to the user
      } else if (err.request) {
        console.error("Error request:", err.request);
        alert("Request error: Unable to reach the backend.");
      } else {
        console.error("General Error:", err.message);
        alert("An unexpected error occurred.");
      }
    }
  };

  useEffect(() => {
    fetchPlayers();
    fetchVenues();
  }, []);

  // Handle player selection
  const handlePlayerSelect = (index, player, team) => {
    if (team === 1) {
      const updatedPlayers = [...playersTeam1];
      updatedPlayers[index] = player;
      setPlayersTeam1(updatedPlayers);
    } else {
      const updatedPlayers = [...playersTeam2];
      updatedPlayers[index] = player;
      setPlayersTeam2(updatedPlayers);
    }
  };

  const detectTournamentType = async (newTournamentType) => {
    try {
      const response = await axios.post(
        `${API_URL}/api/detect_tournament_type`,
        {
          tournament_type: newTournamentType,
        }
      );
      console.log("Tournament Type Details:", response.data);
    } catch (err) {
      console.error(
        "Error detecting tournament type:",
        err.response?.data?.detail || err.message
      );
    }
  };
  const detectMatchDate = async (newMatchDate) => {
    try {
      const response = await axios.post(`${API_URL}/api/detect_date`, {
        match_date: newMatchDate,
      });
      console.log("Match Date:", response.data);
    } catch (err) {
      console.error(
        "Error detecting Match Date:",
        err.response?.data?.detail || err.message
      );
    }
  };

  const handleTournamentTypeChange = (e) => {
    const newTournamentType = e.target.value;
    setTournamentType(newTournamentType);
    detectTournamentType(newTournamentType);
  };

  const handleMatchDateChange = (e) => {
    const date = e.target.value;
    const minDate = new Date("2001-12-19");

    if (new Date(date) <= minDate) {
      setDateError("Date must be after 19th December, 2001.");
    } else {
      setDateError(null); // Clear the error if the date is valid
    }
    setMatchDate(date);
    detectMatchDate(date);
  };

  const loadPlayerOptions = (inputValue, callback) => {
    const availablePlayers = allPlayers.filter(
      (player) =>
        !playersTeam1.includes(player) && !playersTeam2.includes(player)
    );

    const filteredPlayers = availablePlayers.filter((player) =>
      player.label.toLowerCase().includes(inputValue.toLowerCase())
    );
    callback(filteredPlayers.slice(0, 10)); // Limit to 10 filtered results
  };

  const loadVenueOptions = async (inputValue, callback) => {
    const filteredVenues = allVenues.filter((venue) => {
      return venue.name.toLowerCase().includes(inputValue.toLowerCase());
    });
    callback(filteredVenues.slice(0, 10));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if(!need_justification){
      setLoading1(true)
    }else{
      setLoading2(true)
    }

    setError(null);

    try {
      // Validate input data
      if (!team1 || !team2) {
        throw new Error("Please enter both team names.");
      }

      const allPlayersTeam1 = playersTeam1.every(
        (player) => player.label.trim() !== ""
      );
      const allPlayersTeam2 = playersTeam2.every(
        (player) => player.label.trim() !== ""
      );
      if (!allPlayersTeam1 || !allPlayersTeam2) {
        throw new Error("Please enter all player names.");
      }

      // Ensure date is valid before submitting
      if (dateError) {
        throw new Error(dateError);
      }

      // Prepare payload for the backend
      const payload = {
        players_team1: playersTeam1.map((p) => {
          return {
            player_id: p.id,
            player_name: p.name,
            role: p.role,
            team_name: team1.trim(),
          };
        }),
        players_team2: playersTeam2.map((p) => {
          return {
            player_id: p.id,
            player_name: p.name,
            role: p.role,
            team_name: team2.trim(),
          };
        }),
        match_date: matchDate,
        tournament_type: tournamentType,
        venue: venue.trim(),
        need_justification: need_justification,
      };
      // console.log(payload);

      // Make the API call to fetch the recommended team
      const response = await axios.post(
        `${API_URL}/api/recommended_team`,
        payload
      );
      setRecommendedTeam(response.data.recommended_team);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setLoading1(false);
      setLoading2(false);
    }
  };

  // Separate Captains and Vice-Captains from other players
  const captains = recommendedTeam.filter((player) => player.is_captain);
  const viceCaptains = recommendedTeam.filter(
    (player) => player.is_vice_captain
  );
  const otherPlayers = recommendedTeam.filter(
    (player) => !player.is_captain && !player.is_vice_captain
  );

  return (
    <div className="product-ui">
      <h2 className="text-2xl font-bold mb-4">Team Selection Tool</h2>

      <form onSubmit={handleSubmit} className="team-form">
        <div className="flex">
          {/* Left half: Match Date and Tournament Type */}
          <div className="flex-1 mr-2">
            <div className="form-row mb-4">
              <div className="form-group flex-1 mr-2">
                <label className="block mb-1 font-semibold">Match Date:</label>
                <input
                  type="date"
                  value={matchDate}
                  onChange={handleMatchDateChange}
                  required
                  className={`w-full px-3 py-2 border rounded-md ${
                    dateError ? "border-red-500" : ""
                  }`}
                />
                {dateError && (
                  <p className="text-red-500 text-sm">{dateError}</p>
                )}
              </div>
              <div className="form-group flex-1 ml-2">
                <label className="block mb-1 font-semibold">
                  Tournament Type:
                </label>
                <select
                  value={tournamentType}
                  onChange={(e) => handleTournamentTypeChange(e)}
                  className="w-full px-3 py-2 border rounded-md"
                >
                  <option value="T20">T20</option>
                  <option value="ODI">ODI</option>
                  <option value="Test">Test</option>
                </select>
              </div>
            </div>
          </div>

          {/* Right half: Venue */}
          <div className="flex-1 ml-2">
            <label className="mb-1 font-semibold">Venue:</label>
            <AsyncSelect
              loadOptions={loadVenueOptions} // Dynamically fetch options
              value={venue.name}
              onChange={(item) => {
                console.log(item);
                setVenue(item.name);
              }}
              placeholder={`Select Venue`}
              isSearchable
              className="mb-2"
              styles={{
                control: (provided) => ({
                  ...provided,
                  appearance: "none", // Remove the dropdown arrow appearance
                  borderRadius: "5px",
                  boxShadow: "none",
                  borderColor: "#ccc",
                  color: "green",
                }),
              }}
            />
          </div>
        </div>

        <div className="form-row">
          {/* Team 1 Input */}
          <div className="form-group mb-4">
            <label className="block mb-1 font-semibold">Team 1:</label>
            <input
              type="text"
              value={team1}
              onChange={(e) => setTeam1(e.target.value)}
              required
              className="w-full px-3 py-2 border rounded-md"
            />
          </div>

          {/* Team 2 Input */}
          <div className="form-group mb-4">
            <label className="block mb-1 font-semibold">Team 2:</label>
            <input
              type="text"
              value={team2}
              onChange={(e) => setTeam2(e.target.value)}
              required
              className="w-full px-3 py-2 border rounded-md"
            />
          </div>
        </div>
        {/* Players Input */}
        <div className="flex gap-10 mb-4">
          <div className="flex-1">
            <h3 className="text-lg font-semibold mb-2">Players Team 1</h3>
            {playersTeam1.map((player, index) => (
              <AsyncSelect
                loadOptions={loadPlayerOptions} // Dynamically fetch options
                value={playersTeam1[index]}
                onChange={(player) => handlePlayerSelect(index, player, 1)}
                placeholder={`Select Player ${index + 1}`}
                isSearchable
                className="mb-2"
                styles={{
                  control: (provided) => ({
                    ...provided,
                    appearance: "none", // Remove the dropdown arrow appearance
                    borderRadius: "5px",
                    boxShadow: "none",
                    borderColor: "#ccc",
                  }),
                }}
              />
            ))}
          </div>
          <div className="flex-1">
            <h3 className="text-lg font-semibold mb-2">Players Team 2</h3>
            {playersTeam2.map((player, index) => (
              <AsyncSelect
                loadOptions={loadPlayerOptions} // Dynamically fetch options
                value={playersTeam2[index]}
                onChange={(player) => handlePlayerSelect(index, player, 2)}
                placeholder={`Select Player ${index + 1}`}
                isSearchable
                className="custom-select mb-2" // Add a custom class for styling
                styles={{
                  control: (provided) => ({
                    ...provided,
                    appearance: "none", // Remove the dropdown arrow appearance
                    borderRadius: "5px",
                    boxShadow: "none",
                    borderColor: "#ccc",
                  }),
                }}
              />
            ))}
          </div>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          className="submit-button bg-red-600 text-white px-4 py-2 rounded-md"
          disabled={loading1}
          onClick={() => {
            setNeedJustification(false);
            // setLoading1(true);
          }}
        >
          {loading1 ? "Generating Team..." : "Get Recommended Team"}
        </button>
        {error && <p className="error text-red-500 mt-2">{error}</p>}

        {/* Submit Button */}
        <button
          type="submit"
          className="submit-button bg-red-600 text-white px-4 py-2 rounded-md"
          disabled={loading2}
          onClick={() => {
            setNeedJustification(true);
            // setLoading2(true);
          }}
        >
          {loading2 ? "Generating Explanation..." : "Get Explanation"}
        </button>
        {error && <p className="error text-red-500 mt-2">{error}</p>}
      </form>

      {/* Display Recommended Team */}
      {recommendedTeam.length > 0 && (
        <div className="recommended-team mt-10">
          <h2 className="text-2xl font-bold mb-6">Recommended Team</h2>

          {/* First Row: Captain and Vice-Captain */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-6">
            {captains.map((player, index) => (
              <PlayerCard key={index} player={player} team={player.team} />
            ))}
            {viceCaptains.map((player, index) => (
              <PlayerCard key={index} player={player} team={player.team} />
            ))}
          </div>

          {/* Subsequent Rows: Other Players */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
            {otherPlayers.map((player, index) => (
              <PlayerCard key={index} player={player} team={player.team} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default ProductUI;
