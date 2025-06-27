// src/components/PlayerCard.js

import React, { useState } from "react";
import "./PlayerCard.css"; // Ensure this file exists for any additional styling

function PlayerCard({ player, team }) {
  const {
    name,
    role,
    predicted_points,
    justification,
    is_captain,
    is_vice_captain,
  } = player;
  const [showTooltip, setShowTooltip] = useState(false);

  const toggleTooltip = () => {
    setShowTooltip(!showTooltip);
  };

  // Determine border color and glow based on role
  let borderColor = "border-black-600"; // Default red border
  let glowShadow = "shadow-custom-glow"; // Default red glow

  if (is_captain) {
    borderColor = "border-blue-600"; // Blue border for Captain
    glowShadow = "shadow-custom-glow-blue"; // Blue glow
  } else if (is_vice_captain) {
    borderColor = "border-green-600"; // Green border for Vice-Captain
    glowShadow = "shadow-custom-glow-green"; // Green glow
  }

  return (
    <div
      className={`player-card bg-white shadow-lg rounded-lg overflow-hidden relative border-2 ${borderColor} hover:${glowShadow} transition-shadow duration-300`}
    >
      {/* Image Section */}
      {/* <img src={photo} alt={name} className="w-full h-48 object-cover" /> */}

      {/* Content Section */}
      <div className="p-4">
        <h3 className="text-xl font-bold mb-2 flex items-center">
          {name}
          {is_captain && (
            <span className="ml-2 bg-blue-600 text-white text-xs font-semibold px-2 py-1 rounded">
              Captain
            </span>
          )}
          {is_vice_captain && (
            <span className="ml-2 bg-green-600 text-white text-xs font-semibold px-2 py-1 rounded">
              Vice-Captain
            </span>
          )}
        </h3>
        <p className="text-gray-600 mb-1">
          <strong>Role:</strong> {role}
        </p>
        <p className="text-gray-600 mb-1">
          <strong>Team:</strong> {team}
        </p>
        <p className="text-gray-600 mb-3">
          <strong>Predicted Points:</strong> {predicted_points}
        </p>
      </div>

      {/* Tooltip Trigger */}
      <div className="absolute top-2 right-2">
        <button
          className="help-button text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 rounded-full w-8 h-8 flex items-center justify-center"
          onClick={toggleTooltip}
          aria-label={`Why was ${name} selected?`}
        >
          ?
        </button>
        {showTooltip && (
          <div className="absolute right-0 mt-2 w-80 p-2 text-sm text-white bg-black rounded-md shadow-lg">
            {justification}
          </div>
        )}
      </div>
    </div>
  );
}

export default PlayerCard;
