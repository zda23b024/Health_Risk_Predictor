import React, { useState } from "react";

const HealthForm = ({ onSaved }) => {
  const [weight, setWeight] = useState("");
  const [steps, setSteps] = useState("");
  const [waterIntake, setWaterIntake] = useState("");
  const [sleepHours, setSleepHours] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await onSaved({
        weight: parseFloat(weight),
        steps: parseInt(steps, 10),
        water_intake: parseFloat(waterIntake),
        sleep_hours: parseFloat(sleepHours),
      });

      // Reset form after save
      setWeight("");
      setSteps("");
      setWaterIntake("");
      setSleepHours("");
    } catch (err) {
      console.error(err);
      setError("Failed to save entry");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: 400, marginBottom: 20 }}>
      <h2>Daily Health Logger</h2>

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
          Water Intake (liters):
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
          Sleep Hours:
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

      <button type="submit" disabled={loading}>
        {loading ? "Saving..." : "Save Today’s Entry"}
      </button>
    </form>
  );
};

export default HealthForm;
