import React, { useState } from "react";
import { loginUser, resendVerification } from "../api/healthAPI";
import AuthCard from "../components/AuthCard";

const Login = ({ onSuccess, onSwitchToRegister }) => {
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [needsVerification, setNeedsVerification] = useState(false);
  const [verificationEmail, setVerificationEmail] = useState("");
  const [info, setInfo] = useState("");
  const [devLink, setDevLink] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    setInfo("");
    setNeedsVerification(false);
    setLoading(true);
    try {
      const res = await loginUser({ username: identifier, password });
      localStorage.setItem("token", res.data.token);
      onSuccess?.(res.data.user);
    } catch (err) {
      const data = err?.response?.data || {};
      if (err?.response?.status === 403 && data?.needs_verification) {
        setNeedsVerification(true);
        setVerificationEmail(data.email || identifier);
        setError(data.error || "Email not verified");
        if (data.dev_link) setDevLink(data.dev_link);
      } else {
        setError(data.error || "Login failed");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleResend = async () => {
    if (!verificationEmail) return;
    setLoading(true);
    setError("");
    setInfo("");
    try {
      const res = await resendVerification({ email: verificationEmail });
      setInfo(res.data.message || "Verification email resent.");
      setNeedsVerification(false);
    } catch (err) {
      setError(err?.response?.data?.error || "Failed to resend verification");
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthCard
      title="Sign in"
      subtitle="Sign in to your account"
      hintText="No account?"
      hintButtonLabel="Create one"
      onHintAction={onSwitchToRegister}
    >
      <form onSubmit={submit}>
        <div className="field">
          <label>Username or Email</label>
          <input
            value={identifier}
            onChange={(e) => setIdentifier(e.target.value)}
            placeholder="Username or email"
            required
          />
        </div>

        <div className="field">
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••"
            required
          />
        </div>

        <button
          className="btn btnPrimary"
          style={{ width: "100%" }}
          disabled={loading}
        >
          {loading ? "Signing in..." : "Sign in"}
        </button>

        {info ? <div className="card" style={{ marginTop: 12, background: 'rgba(237, 247, 255, 0.9)', border: '1px solid rgba(37,99,235,0.09)' }}>{info}</div> : null}

        {needsVerification && (
          <div className="card" style={{ marginTop: 12, padding: 12, display: 'flex', gap: 10, alignItems: 'center' }}>
            <div style={{ flex: 1 }}>
              <div style={{ fontWeight: 700 }}>Email not verified</div>
              <div className="hint">A verification email was sent to <strong>{verificationEmail}</strong>. Click resend to send another.</div>
              {devLink ? (
                <div style={{ marginTop: 8 }}>
                  <div style={{ fontWeight: 700 }}>Developer verification link (dev only)</div>
                  <a href={devLink} target="_blank" rel="noopener noreferrer" className="btn" style={{ padding: '8px 12px', marginTop: 6 }}>Open link</a>
                </div>
              ) : null}
            </div>
            <div>
              <button type="button" className="btn btnPrimary" onClick={handleResend} disabled={loading}>Resend</button>
            </div>
          </div>
        )}

        {error && <div className="error">{error}</div>}
      </form>
    </AuthCard>
  );
};

export default Login;
