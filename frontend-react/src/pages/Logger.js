import React, { useEffect, useState } from "react";
import HealthForm from "../components/HealthForm";
import { getHealthEntries, addHealthEntry } from "../api/healthAPI";

const Logger = () => {
  const [entries, setEntries] = useState([]);
  const [loadingEntries, setLoadingEntries] = useState(false);
  const [loadError, setLoadError] = useState("");
  const [view, setView] = useState("logger"); // 'logger' (form-only) | 'today' | 'past' (controls which sections are visible)

  const todayISO = new Date().toISOString().slice(0, 10); // YYYY-MM-DD

  const loadEntries = async () => {
    setLoadingEntries(true);
    setLoadError("");

    try {
      const res = await getHealthEntries(7);
      setEntries(res.data);
    } catch (err) {
      console.error(err);
      setLoadError("Failed to load entries");
    } finally {
      setLoadingEntries(false);
    }
  };

  useEffect(() => {
    loadEntries();
  }, []);

  const handleSave = async (entry) => {
    // Add entry_date = today by default
    await addHealthEntry({ ...entry, entry_date: todayISO });
    await loadEntries();
  };

  const todaysEntry = entries.find((e) => e.entry_date === todayISO);
  const pastEntries = entries.filter((e) => e.entry_date !== todayISO);

  return (
    <div className="container loggerPage">
      <div className="card loggerCard">
        {view === "logger" && <HealthForm onSaved={handleSave} />}

        <hr />

        <div className="entrySection">
          {view === "today" && (
            <>
              <h2>Today&apos;s Entry ({todayISO})</h2>

              {todaysEntry ? (
                <div className="entryCard todayCard">
                  <div className="entryCardHeader">
                    <div className="entryDate">Today · {todayISO}</div>
                    <div className="badge">Today</div>
                  </div>

                  <div className="metrics">
                    <div className="metric">
                      <div className="mLabel">Weight</div>
                      <div className="mValue">{todaysEntry.weight} kg</div>
                    </div>
                    <div className="metric">
                      <div className="mLabel">Steps</div>
                      <div className="mValue">{todaysEntry.steps}</div>
                    </div>
                    <div className="metric">
                      <div className="mLabel">Water</div>
                      <div className="mValue">{todaysEntry.water_intake} L</div>
                    </div>
                    <div className="metric">
                      <div className="mLabel">Sleep</div>
                      <div className="mValue">{todaysEntry.sleep_hours} h</div>
                    </div>
                  </div>
                </div>
              ) : (
                <p className="hint">No entry yet for today.</p>
              )}
            </>
          )}

          {view === "past" && (
            <>
              <h2>Past Entries (Last 7 Days)</h2>
              {loadingEntries ? (
                <p className="hint">Loading entries...</p>
              ) : loadError ? (
                <p className="error">{loadError}</p>
              ) : pastEntries.length === 0 ? (
                <p className="hint">No past entries.</p>
              ) : (
                <ul className="entryList">
                  {pastEntries.map((e) => (
                    <li className="entryCard" key={e.id}>
                      <div className="entryCardHeader">
                        <div className="entryDate">{e.entry_date}</div>
                        {e.entry_date === todayISO && <div className="badge">Today</div>}
                      </div>

                      <div className="metrics">
                        <div className="metric">
                          <div className="mLabel">Weight</div>
                          <div className="mValue">{e.weight} kg</div>
                        </div>
                        <div className="metric">
                          <div className="mLabel">Steps</div>
                          <div className="mValue">{e.steps}</div>
                        </div>
                        <div className="metric">
                          <div className="mLabel">Water</div>
                          <div className="mValue">{e.water_intake} L</div>
                        </div>
                        <div className="metric">
                          <div className="mLabel">Sleep</div>
                          <div className="mValue">{e.sleep_hours} h</div>
                        </div>
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </>
          )}
        </div>

        <div className="cardFooter">
          {view === "logger" ? (
            <>
              <button
                type="button"
                className={`btn btnPrimary`}
                onClick={() => setView("today")}
              >
                Today&apos;s Entries
              </button>

              <button
                type="button"
                className={`btn btnPrimary`}
                onClick={() => setView("past")}
              >
                Past Entries
              </button>
            </>
          ) : (
            <>
              <button
                type="button"
                className={`btn btnPrimary`}
                onClick={() => setView("logger")}
              >
                Back to Logger
              </button>

              <button
                type="button"
                className={`btn btnPrimary`}
                onClick={() => setView(view === "today" ? "past" : "today")}
              >
                {view === "today" ? "Past Entries" : "Today\'s Entries"}
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default Logger;
