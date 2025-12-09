import React, { useEffect, useState } from "react";
import { getHealthStats } from "../api/healthAPI";
import TrendCharts from "../components/TrendCharts";
import SummaryCards from "../components/SummaryCards";

const Trends = () => {
  const [weightTrend, setWeightTrend] = useState([]);
  const [stepsTrend, setStepsTrend] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadStats = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await getHealthStats();
      setWeightTrend(res.data.weight_trend || []);
      setStepsTrend(res.data.steps_trend || []);
      setSummary(res.data.summary || null);
    } catch (err) {
      console.error(err);
      setError("Failed to load stats");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadStats();
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>Trends Visualizer (Module 2)</h1>

      {loading && <p>Loading stats...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {!loading && !error && (
        <>
          <SummaryCards summary={summary} />
          <TrendCharts weightTrend={weightTrend} stepsTrend={stepsTrend} />
        </>
      )}
    </div>
  );
};

export default Trends;
