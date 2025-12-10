import React from "react";
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

const TrendCharts = ({ weightTrend, stepsTrend }) => {
  return (
    <div style={{ display: "grid", gap: "30px", marginTop: "20px" }}>
      {/* Weight Trend Line Chart */}
      <div style={{ width: "100%", height: 300 }}>
        <h2>Weight Trend (Last 7 Days)</h2>
        {weightTrend && weightTrend.length > 0 ? (
          <ResponsiveContainer>
            <LineChart data={weightTrend}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="entry_date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey="weight"
                name="Weight (kg)"
                dot
              />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <p>No data to display.</p>
        )}
      </div>

      {/* Steps Bar Chart */}
      <div style={{ width: "100%", height: 300 }}>
        <h2>Daily Steps (Last 7 Days)</h2>
        {stepsTrend && stepsTrend.length > 0 ? (
          <ResponsiveContainer>
            <BarChart data={stepsTrend}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="entry_date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="steps" name="Steps" />
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <p>No data to display.</p>
        )}
      </div>
    </div>
  );
};

export default TrendCharts;
