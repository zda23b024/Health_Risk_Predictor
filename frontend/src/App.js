import React, { useState } from "react";
import Logger from "./pages/Logger";
import Trends from "./pages/Trends";

function App() {
  const [activePage, setActivePage] = useState("logger");

  return (
    <div>
      <header
        style={{
          padding: 20,
          borderBottom: "1px solid #ccc",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <h1>HealthTracker</h1>
        <nav style={{ display: "flex", gap: "10px" }}>
          <button
            onClick={() => setActivePage("logger")}
            style={{
              padding: "8px 12px",
              borderRadius: "6px",
              border: "1px solid #ccc",
              background:
                activePage === "logger" ? "#e0f7fa" : "white",
            }}
          >
            Daily Logger (M1)
          </button>
          <button
            onClick={() => setActivePage("trends")}
            style={{
              padding: "8px 12px",
              borderRadius: "6px",
              border: "1px solid #ccc",
              background:
                activePage === "trends" ? "#e0f7fa" : "white",
            }}
          >
            Trends (M2)
          </button>
        </nav>
      </header>

      <main>
        {activePage === "logger" && <Logger />}
        {activePage === "trends" && <Trends />}
      </main>
    </div>
  );
}

export default App;
