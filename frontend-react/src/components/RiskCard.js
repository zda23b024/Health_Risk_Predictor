import React from "react";

const badgeStyle = (label) => {
  if (label === "High") return { background: "rgba(239,68,68,0.12)", borderColor: "rgba(239,68,68,0.35)", color: "#991b1b" };
  if (label === "Medium") return { background: "rgba(245,158,11,0.12)", borderColor: "rgba(245,158,11,0.35)", color: "#92400e" };
  return { background: "rgba(34,197,94,0.12)", borderColor: "rgba(34,197,94,0.35)", color: "#065f46" };
};

// Map recommendation text to helpful external resources or actions
const getActionsForRecommendation = (text) => {
  const t = text.toLowerCase();
  const actions = [];
  if (t.includes("check-up") || t.includes("healthcare provider") || t.includes("schedule")) {
    actions.push({ label: "Find a provider", url: "https://www.healthgrades.com/" });
  }
  if (t.includes("sleep")) {
    actions.push({ label: "Sleep tips", url: "https://www.cdc.gov/sleep/about_sleep/sleep_hygiene.html" });
  }
  if (t.includes("hydration") || t.includes("water")) {
    actions.push({ label: "Hydration tips", url: "https://www.nhs.uk/live-well/eat-well/water-drinks-nutrition/" });
  }
  if (t.includes("activity") || t.includes("steps") || t.includes("exercise") || t.includes("strength")) {
    actions.push({ label: "Activity guidelines", url: "https://www.who.int/news-room/fact-sheets/detail/physical-activity" });
  }
  if (t.includes("diet") || t.includes("weight") || t.includes("dietitian")) {
    actions.push({ label: "Nutrition advice", url: "https://www.eatright.org/" });
  }
  return actions;
};

const LinkButton = ({ url, label }) => (
  <a className="linkBtn btn" href={url} target="_blank" rel="noopener noreferrer" style={{ display: "inline-block", marginLeft: 8, fontSize: 13 }}>
    {label}
  </a>
);

const RiskCard = ({ result }) => {
  if (!result) return null;

  const intro = `Based on the inputs (weight ${result.inputs.weight} kg, height ${result.inputs.height} cm, steps ${result.inputs.steps}, sleep ${result.inputs.sleep_hours} hrs), here are practical suggestions you can try.`;

  return (
    <div style={{ marginTop: 18 }}>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 12,
          flexWrap: "wrap",
        }}
      >
        <div
          style={{
            padding: "8px 12px",
            borderRadius: 999,
            border: "1px solid",
            fontWeight: 800,
            ...badgeStyle(result.risk_label),
          }}
        >
          Risk: {result.risk_label}
        </div>
        <div style={{ color: "#6b7280", fontSize: 13 }}>
          BMI: <strong>{result.bmi}</strong> • Model: <strong>{String(result.used_model)}</strong>
        </div>
      </div>

      <div style={{ marginTop: 14 }}>
        <div style={{ fontWeight: 800, marginBottom: 8 }}>Personalized Recommendations</div>
        <div className="hint" style={{ marginBottom: 10 }}>{intro}</div>

        <ul className="recommendationList">
          {(result.recommendations || []).map((r, idx) => {
            const actions = getActionsForRecommendation(r);
            return (
              <li key={idx} className="recItem">
                <div className="recText">{r}</div>
                {actions.length > 0 && (
                  <div className="recActions">
                    {actions.map((a, i) => <LinkButton key={i} url={a.url} label={a.label} />)}
                  </div>
                )}
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  );
};

export default RiskCard;
