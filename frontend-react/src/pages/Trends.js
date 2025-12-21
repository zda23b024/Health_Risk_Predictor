import React, { useEffect, useState } from "react";
import { getHealthStats } from "../api/healthAPI";
import SummaryCards from "../components/SummaryCards";

// Recharts components used inline below
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  BarChart,
  Bar,
  Legend,
  ResponsiveContainer,
} from "recharts";

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
      <h1>Trends Visualizer</h1>

      {loading && <p>Loading stats...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {!loading && !error && (
        <div className="trendsGrid threeCol">
          <div className="summaryColumn panel">
            <SummaryCards summary={summary} />
          </div>

          <div className="weightColumn panel">
            <div className="chartCard weightChart">
              <h2>Weight Trend (Last 7 Days)</h2>
              {weightTrend && weightTrend.length > 0 ? (
                <div className="chartInner">
                  <ResponsiveContainer>
                    <LineChart data={weightTrend}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="entry_date" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Line type="monotone" dataKey="weight" name="Weight (kg)" dot />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              ) : (
                <p>No data to display.</p>
              )}
            </div>
          </div>

          <div className="stepsColumn panel">
            <div className="chartCard stepsChart">
              <h2>Daily Steps (Last 7 Days)</h2>
              {stepsTrend && stepsTrend.length > 0 ? (
                <div className="chartInner">
                  <ResponsiveContainer>
                    <BarChart data={stepsTrend}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="entry_date" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Bar dataKey="steps" name="Steps" fill="#3b82f6" radius={[6, 6, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              ) : (
                <p>No data to display.</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Trends;
