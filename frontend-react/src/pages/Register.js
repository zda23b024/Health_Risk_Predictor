import React, { useState } from "react";
import { registerUser } from "../api/healthAPI";
import AuthCard from "../components/AuthCard";

const Register = ({ onSuccess, onSwitchToLogin }) => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [info, setInfo] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    setInfo("");
    setLoading(true);
    try {
      const res = await registerUser({ username, email, password });
      // Auto-login on registration (no email verification required)
      if (res.data?.token) {
        localStorage.setItem("token", res.data.token);
        onSuccess?.(res.data.user);
      } else {
        setInfo(res.data.message || "Registered. You can now log in.");
      }
    } catch (err) {
      setError(err?.response?.data?.error || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthCard
      title="Create account"
      subtitle="Username ≥ 3 chars, password ≥ 4 chars"
      hintText="Already have an account?"
      hintButtonLabel="Sign in"
      onHintAction={onSwitchToLogin}
    >
      <form onSubmit={submit}>
        <div className="field">
          <label>Username</label>
          <input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="e.g., abdallah" />
        </div>
        <div className="field">
          <label>Email</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" required />
        </div>
        <div className="field">
          <label>Password</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••" />
        </div>

        <button className="btn btnPrimary" style={{ width: "100%" }} disabled={loading}>
          {loading ? "Creating..." : "Create account"}
        </button>

        {error ? <div className="error">{error}</div> : null}
        {info ? <div className="card" style={{ marginTop: 12, background: 'rgba(237, 247, 255, 0.9)', border: '1px solid rgba(37,99,235,0.09)' }}>{info}</div> : null}

      </form>
    </AuthCard>
  );
};

export default Register;
