import React from "react";

const AuthCard = ({ title, subtitle, children, hintText, hintButtonLabel, onHintAction }) => {
  return (
    <div className="authWrap">
      <div className="card authCard">
        <div className="brand" style={{ marginBottom: 12 }}>
          <div className="logo" />
          <div>
            <div style={{ fontSize: 18, fontWeight: 800 }}>{title}</div>
            <div className="hint">{subtitle}</div>
          </div>
        </div>

        {children}

        {hintText && hintButtonLabel && (
          <div className="hint" style={{ marginTop: 12 }}>
            {hintText}
            <button type="button" className="btn" onClick={onHintAction} style={{ padding: "6px 10px", marginLeft: 8 }}>
              {hintButtonLabel}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default AuthCard;
