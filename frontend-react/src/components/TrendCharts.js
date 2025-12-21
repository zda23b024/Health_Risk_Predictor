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
      <div className="chartCard weightChart">
        <h2>Weight Trend (Last 7 Days)</h2>
        {weightTrend && weightTrend.length > 0 ? (
          <div className="chartInner">
            <ResponsiveContainer>
              <LineChart data={weightTrend}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="entry_date" tick={{ fontSize: 14 }} />
                <YAxis tick={{ fontSize: 14 }} />
                <Tooltip />
                <Legend wrapperStyle={{ fontSize: 13 }} />
                <Line
                  type="monotone"
                  dataKey="weight"
                  name="Weight (kg)"
                  dot
                  strokeWidth={3}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        ) : (
          <p>No data to display.</p>
        )}
      </div>

      {/* Steps Bar Chart */}
      <div className="chartCard stepsChart">
        <h2>Daily Steps (Last 7 Days)</h2>
        {stepsTrend && stepsTrend.length > 0 ? (
          <div className="chartInner">
            <ResponsiveContainer>
              <BarChart data={stepsTrend}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="entry_date" tick={{ fontSize: 14 }} />
                <YAxis tick={{ fontSize: 14 }} />
                <Tooltip />
                <Legend wrapperStyle={{ fontSize: 13 }} />
                <Bar dataKey="steps" name="Steps" fill="#2563eb" radius={[8, 8, 0, 0]} barSize={72} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        ) : (
          <p>No data to display.</p>
        )}
      </div>
    </div>
  );
};

export default TrendCharts;
