import React, { useState } from "react";
import { predictHealthRisk } from "../api/healthAPI";
import RiskCard from "../components/RiskCard";

const Predictor = () => {
  const [weight, setWeight] = useState("");
  const [steps, setSteps] = useState("");
  const [waterIntake, setWaterIntake] = useState("");
  const [sleepHours, setSleepHours] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    setResult(null);

    try {
      const payload = {
        weight: parseFloat(weight),
        steps: parseInt(steps, 10),
        water_intake: parseFloat(waterIntake),
        sleep_hours: parseFloat(sleepHours),
      };

      const res = await predictHealthRisk(payload);
      setResult(res.data);
    } catch (err) {
      console.error(err);
      setError(
        "Failed to get prediction. Check backend /health/predict and decision_tree.pkl."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Health Risk Predictor (Module 3)</h1>

      <form
        onSubmit={handleSubmit}
        style={{ maxWidth: "400px", marginTop: "20px" }}
      >
        <div>
          <label>
            Weight (kg):
            <input
              type="number"
              step="0.1"
              value={weight}
              onChange={(e) => setWeight(e.target.value)}
              required
            />
          </label>
        </div>

        <div>
          <label>
            Steps:
            <input
              type="number"
              value={steps}
              onChange={(e) => setSteps(e.target.value)}
              required
            />
          </label>
        </div>

        <div>
          <label>
            Water Intake (L/day):
            <input
              type="number"
              step="0.1"
              value={waterIntake}
              onChange={(e) => setWaterIntake(e.target.value)}
              required
            />
          </label>
        </div>

        <div>
          <label>
            Sleep Hours (per night):
            <input
              type="number"
              step="0.1"
              value={sleepHours}
              onChange={(e) => setSleepHours(e.target.value)}
              required
            />
          </label>
        </div>

        {error && <p style={{ color: "red" }}>{error}</p>}

        <button
          type="submit"
          disabled={loading}
          style={{ marginTop: "10px" }}
        >
          {loading ? "Predicting..." : "Predict Risk"}
        </button>
      </form>

      {result && (
        <RiskCard
          riskLabel={result.risk_label}
          probabilities={result.probabilities}
        />
      )}
    </div>
  );
};

export default Predictor;
