import React, { useEffect, useState } from "react";
import Logger from "./pages/Logger";
import Trends from "./pages/Trends";
import Predictor from "./pages/Predictor"; // ✅ ADD AI MODULE
import Login from "./pages/Login";
import Register from "./pages/Register";
import "./App.css";

function App() {
  const [activePage, setActivePage] = useState("logger");
  const [isAuthed, setIsAuthed] = useState(!!localStorage.getItem("token"));
  const [authView, setAuthView] = useState("login");

  useEffect(() => {
    setIsAuthed(!!localStorage.getItem("token"));
  }, []);

  const handleAuthSuccess = () => {
    setIsAuthed(true);
    setActivePage("logger");
  };

  const logout = () => {
    const ok = window.confirm("You are about to log out. Do you want to continue?");
    if (!ok) return; // user cancelled
    localStorage.removeItem("token");
    setIsAuthed(false);
    setAuthView("login");
  };

  if (!isAuthed) {
    return authView === "register" ? (
      <Register onSuccess={handleAuthSuccess} onSwitchToLogin={() => setAuthView("login")} />
    ) : (
      <Login onSuccess={handleAuthSuccess} onSwitchToRegister={() => setAuthView("register")} />
    );
  }

  return (
    <div className="container">
      <header className="topbar">
        <div className="brand">
          <div className="logo" />
          <div>
            <div style={{ fontSize: 20, fontWeight: 900 }}>HealthTracker</div>
            <div className="hint">Wellness logger • trends • risk predictor</div>
          </div>
        </div>

        <div className="nav">
          <button
            onClick={() => setActivePage("logger")}
            className={`btn ${activePage === "logger" ? "btnActive" : ""}`}
          >
            Daily Logger
          </button>
          <button
            onClick={() => setActivePage("trends")}
            className={`btn ${activePage === "trends" ? "btnActive" : ""}`}
          >
            Trends
          </button>
          <button
            onClick={() => setActivePage("predict")}
            className={`btn ${activePage === "predict" ? "btnActive" : ""}`}
          >
            Health Risk (AI)
          </button>
          <div className="spacer" />
          <button onClick={logout} className="btn">
            Logout
          </button>
        </div>
      </header>

      <main style={{ marginTop: 12 }}>
        <div className="card">
          {activePage === "logger" && <Logger />}
          {activePage === "trends" && <Trends />}
          {activePage === "predict" && <Predictor />}
        </div>
      </main>
    </div>
  );
}

export default App;
