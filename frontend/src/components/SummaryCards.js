import React from "react";

const cardStyle = {
  padding: "15px 20px",
  borderRadius: "8px",
  border: "1px solid #ddd",
  background: "#fafafa",
  minWidth: "180px",
};

const SummaryCards = ({ summary }) => {
  if (!summary) {
    return null;
  }

  const {
    min_weight,
    max_weight,
    avg_weight,
    avg_steps,
    avg_water_intake,
    avg_sleep_hours,
    data_points,
  } = summary;

  return (
    <div style={{ marginTop: "20px" }}>
      <h2>Summary (Last {data_points || 0} Entries)</h2>
      {data_points === 0 ? (
        <p>No data available for summary.</p>
      ) : (
        <div
          style={{
            display: "flex",
            flexWrap: "wrap",
            gap: "15px",
            marginTop: "10px",
          }}
        >
          <div style={cardStyle}>
            <h3>Weight</h3>
            <p>Avg: {avg_weight?.toFixed(1)} kg</p>
            <p>Min: {min_weight} kg</p>
            <p>Max: {max_weight} kg</p>
          </div>

          <div style={cardStyle}>
            <h3>Steps</h3>
            <p>Avg: {avg_steps?.toFixed(0)}</p>
          </div>

          <div style={cardStyle}>
            <h3>Water Intake</h3>
            <p>Avg: {avg_water_intake?.toFixed(1)} L/day</p>
          </div>

          <div style={cardStyle}>
            <h3>Sleep</h3>
            <p>Avg: {avg_sleep_hours?.toFixed(1)} h/night</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default SummaryCards;
