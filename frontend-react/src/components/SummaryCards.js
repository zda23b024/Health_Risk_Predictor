import React from "react";

const cardStyle = {
  padding: "12px 14px",
  borderRadius: "10px",
  border: "1px solid rgba(37,99,235,0.08)",
  background: "linear-gradient(180deg, rgba(232,246,255,1), rgba(243,250,255,1))",
  width: "100%", // fill the summary column
  boxShadow: "0 6px 14px rgba(37,99,235,0.03)",
};


const fmt = (v, digits) =>
  v != null && !Number.isNaN(Number(v)) ? Number(v).toFixed(digits) : "-";

const SummaryCards = ({ summary }) => {
  if (!summary) return null;

  const {
    data_points,

    avg_weight, min_weight, max_weight,
    avg_steps, min_steps, max_steps,
    avg_water_intake, min_water_intake, max_water_intake,
    avg_sleep_hours, min_sleep_hours, max_sleep_hours,
  } = summary;

  return (
    <div style={{ marginTop: "20px" }} className="summaryWrap">
      <h2>Summary</h2>

      {data_points === 0 ? (
        <p>No data available.</p>
      ) : (
        <div className="summaryGrid" style={{ marginTop: 12 }}>

          {/* Weight */}
          <div style={cardStyle} className="summaryCard">
            <h3>Weight (kg)</h3>
            <div className="summaryAvg"><span className="avgLabel">Avg</span><span className="avgValue">{fmt(avg_weight, 1)}</span></div>
            <p className="muted">Min: {fmt(min_weight, 1)} · Max: {fmt(max_weight, 1)}</p>
          </div>

          {/* Steps */}
          <div style={cardStyle} className="summaryCard">
            <h3>Steps</h3>
            <div className="summaryAvg"><span className="avgLabel">Avg</span><span className="avgValue">{fmt(avg_steps, 0)}</span></div>
            <p className="muted">Min: {fmt(min_steps, 0)} · Max: {fmt(max_steps, 0)}</p>
          </div>

          {/* Water */}
          <div style={cardStyle} className="summaryCard">
            <h3>Water Intake (L)</h3>
            <div className="summaryAvg"><span className="avgLabel">Avg</span><span className="avgValue">{fmt(avg_water_intake, 1)}</span></div>
            <p className="muted">Min: {fmt(min_water_intake, 1)} · Max: {fmt(max_water_intake, 1)}</p>
          </div>

          {/* Sleep */}
          <div style={cardStyle} className="summaryCard">
            <h3>Sleep (hours)</h3>
            <div className="summaryAvg"><span className="avgLabel">Avg</span><span className="avgValue">{fmt(avg_sleep_hours, 1)}</span></div>
            <p className="muted">Min: {fmt(min_sleep_hours, 1)} · Max: {fmt(max_sleep_hours, 1)}</p>
          </div>

        </div>
      )}
    </div>
  );
};

export default SummaryCards;
