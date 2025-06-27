// src/components/ModelUI.js

import React, { useState } from "react";
import axios from "axios";
import "./ModelUI.css";

function ModelUI() {
  const [trainingStart, setTrainingStart] = useState("");
  const [trainingEnd, setTrainingEnd] = useState("");
  const [testingStart, setTestingStart] = useState("");
  const [testingEnd, setTestingEnd] = useState("");
  const [performanceData, setPerformanceData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Prepare payload
      const payload = {
        training_start: trainingStart,
        training_end: trainingEnd,
        testing_start: testingStart,
        testing_end: testingEnd,
      };

      // Make API call to analyze model performance
      const response = await axios.post(
        "http://127.0.0.1:8000/api/analyze_model",
        payload
      );
      setPerformanceData(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async () => {
    try {
      // API call to download the model
      const response = await axios.get(
        "http://127.0.0.1:8000/api/download_model",
        {
          responseType: "blob",
        }
      );
      // Handle file download
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "model_with_results.zip");
      document.body.appendChild(link);
      link.click();
    } catch (err) {
      console.error("Error downloading model:", err);
    }
  };

  const handleRetrain = async () => {
    try {
      setLoading(true);
      // API call to retrain the model
      await axios.post("http://127.0.0.1:8000/api/retrain_model");
      alert("Model retraining initiated.");
    } catch (err) {
      console.error("Error retraining model:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="model-ui">
      <h2>Model Performance Analysis</h2>
      <form onSubmit={handleAnalyze} className="model-form">
        <div className="form-row">
          <div className="form-group">
            <label>Training Start Date:</label>
            <input
              type="date"
              value={trainingStart}
              onChange={(e) => setTrainingStart(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Training End Date:</label>
            <input
              type="date"
              value={trainingEnd}
              onChange={(e) => setTrainingEnd(e.target.value)}
              required
            />
          </div>
        </div>
        <div className="form-row">
          <div className="form-group">
            <label>Testing Start Date:</label>
            <input
              type="date"
              value={testingStart}
              onChange={(e) => setTestingStart(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Testing End Date:</label>
            <input
              type="date"
              value={testingEnd}
              onChange={(e) => setTestingEnd(e.target.value)}
              required
            />
          </div>
        </div>
        <button type="submit" className="submit-button" disabled={loading}>
          {loading ? "Analyzing..." : "Analyze Performance"}
        </button>
        {error && <p className="error">{error}</p>}
      </form>

      {performanceData && (
        <div className="performance-results">
          <h3>Performance Metrics</h3>
          <table>
            <thead>
              <tr>
                <th>Metric</th>
                <th>Value</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(performanceData).map(([metric, value], index) => (
                <tr key={index}>
                  <td>{metric}</td>
                  <td>{value}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="buttons">
            <button onClick={handleDownload} className="download-button">
              Download Model
            </button>
            <button onClick={handleRetrain} className="retrain-button">
              Retrain Model
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default ModelUI;
