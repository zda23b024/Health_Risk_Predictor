import React, { useEffect, useState } from "react";
import HealthForm from "../components/HealthForm";
import { getHealthEntries, addHealthEntry } from "../api/healthAPI";

const Logger = () => {
  const [entries, setEntries] = useState([]);
  const [loadingEntries, setLoadingEntries] = useState(false);
  const [loadError, setLoadError] = useState("");

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
    <div style={{ padding: 20 }}>
      <HealthForm onSaved={handleSave} />

      <hr />

      <h2>Today&apos;s Entry ({todayISO})</h2>
      {todaysEntry ? (
        <div>
          <p>Weight: {todaysEntry.weight} kg</p>
          <p>Steps: {todaysEntry.steps}</p>
          <p>Water Intake: {todaysEntry.water_intake} L</p>
          <p>Sleep Hours: {todaysEntry.sleep_hours}</p>
        </div>
      ) : (
        <p>No entry yet for today.</p>
      )}

      <hr />

      <h2>Past Entries (Last 7 Days)</h2>
      {loadingEntries ? (
        <p>Loading entries...</p>
      ) : loadError ? (
        <p style={{ color: "red" }}>{loadError}</p>
      ) : pastEntries.length === 0 ? (
        <p>No past entries.</p>
      ) : (
        <ul>
          {pastEntries.map((e) => (
            <li key={e.id}>
              <strong>{e.entry_date}</strong> – Weight: {e.weight} kg, Steps:{" "}
              {e.steps}, Water: {e.water_intake} L, Sleep: {e.sleep_hours} h
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Logger;
