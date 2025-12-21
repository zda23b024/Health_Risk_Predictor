import React, { useState } from "react";
import { predictHealthRisk } from "../api/healthAPI";
import RiskCard from "../components/RiskCard";

const Predictor = () => {
  const [weight, setWeight] = useState("");
  const [height, setHeight] = useState("");
  const [steps, setSteps] = useState("");
  const [sleep, setSleep] = useState("");
  const [waterIntake, setWaterIntake] = useState("");

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
        height: parseFloat(height),
        steps: parseInt(steps, 10),
        water_intake: parseFloat(waterIntake),
        sleep_hours: parseFloat(sleep),
      };

      const res = await predictHealthRisk(payload);
      setResult(res.data);
    } catch (err) {
      console.error(err);
      setError(
        "Failed to get prediction. Check backend /health/predict and random_forest.pkl."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Health Risk Predictor</h1>
      <p style={{ color: "#6b7280" }}>
        Uses BMI (weight + height), sleep hours, and steps to classify risk as Low/Medium/High.
      </p>

      <div className="predictWrap">
        <div className="predictLeft">
          <form onSubmit={handleSubmit} className="predictForm">
            <div className="field">
              <label>Weight (kg)</label>
              <input type="number" step="0.1" value={weight} onChange={(e) => setWeight(e.target.value)} required />
            </div>

            <div className="field">
              <label>Height (cm)</label>
              <input type="number" step="0.1" value={height} onChange={(e) => setHeight(e.target.value)} required />
            </div>

            <div className="field">
              <label>Steps</label>
              <input type="number" value={steps} onChange={(e) => setSteps(e.target.value)} required />
            </div>

            <div className="field">
              <label>Water Intake (L)</label>
              <input type="number" step="0.1" value={waterIntake} onChange={(e) => setWaterIntake(e.target.value)} required />
            </div>

            <div className="field">
              <label>Sleep hours</label>
              <input type="number" step="0.1" value={sleep} onChange={(e) => setSleep(e.target.value)} required />
            </div>

            {error && <p style={{ color: "red" }}>{error}</p>}

            <button type="submit" disabled={loading} className="btn btnPrimary" style={{ marginTop: 6 }}>
              {loading ? "Predicting..." : "Predict Risk"}
            </button>
          </form>
        </div>

        <div className="predictRight">
          <div className="resultPanel card">
            {result ? (
              <RiskCard result={result} />
            ) : (
              <div style={{ padding: 18 }}>
                <div style={{ fontWeight: 800, fontSize: 18, marginBottom: 10 }}>Prediction</div>
                <p className="hint">Prediction results will appear here after you click <strong>Predict Risk</strong>.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Predictor;
