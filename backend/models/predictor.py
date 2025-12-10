"""
predictor.py

Module 3: Health Risk Predictor - Model Loader & Predictor

Loads the trained Decision Tree model from decision_tree.pkl
and exposes a simple function to predict the health risk level
(Low / Medium / High) based on user input features.
"""

from pathlib import Path
from typing import Dict, Any

import joblib
import numpy as np

# Path to model file: backend/ml/decision_tree.pkl
BASE_DIR = Path(__file__).resolve().parent.parent  # backend/
MODEL_PATH = BASE_DIR / "ml" / "decision_tree.pkl"


class HealthRiskPredictor:
    def __init__(self, model_path: Path):
        if not model_path.exists():
            raise FileNotFoundError(
                f"Model file not found at: {model_path}. "
                f"Please train the model with ml/train_model.py first."
            )

        saved = joblib.load(model_path)
        self.model = saved["model"]
        self.label_encoder = saved["label_encoder"]

    def predict(self, weight: float, steps: int, water_intake: float, sleep_hours: float) -> Dict[str, Any]:
        """
        Predict the risk label and return both the label and probabilities.
        """
        # Prepare a 2D array with one sample: shape (1, 4)
        features = np.array([[weight, steps, water_intake, sleep_hours]], dtype=float)

        # Predict class index
        class_idx = self.model.predict(features)[0]
        risk_label = self.label_encoder.inverse_transform([class_idx])[0]

        # Predict probabilities (for all classes)
        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(features)[0]  # shape (n_classes,)
            # Map each class label to its probability
            class_labels = self.label_encoder.inverse_transform(
                np.arange(len(probs))
            )
            probabilities = {
                label: float(prob)
                for label, prob in zip(class_labels, probs)
            }
        else:
            probabilities = {}

        return {
            "risk_label": risk_label,
            "probabilities": probabilities,
        }


# Singleton-style predictor instance (loaded at import time)
_predictor_instance: HealthRiskPredictor | None = None


def get_predictor() -> HealthRiskPredictor:
    """
    Lazily initialize and return a singleton HealthRiskPredictor instance.
    """
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = HealthRiskPredictor(MODEL_PATH)
    return _predictor_instance
