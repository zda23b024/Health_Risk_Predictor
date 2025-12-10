import React from "react";
import Logger from "./pages/Logger";

function App() {
  return (
    <div>
      <header style={{ padding: 20, borderBottom: "1px solid #ccc" }}>
        <h1>HealthTracker - Daily Logger (Module 1)</h1>
      </header>
      <main>
        <Logger />
      </main>
    </div>
  );
}

export default App;
