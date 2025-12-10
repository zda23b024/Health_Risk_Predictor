from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "health_data.csv"
MODEL_PATH = BASE_DIR / "decision_tree.pkl"

RANDOM_STATE = 42
TEST_SIZE = 0.2


def load_data(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset not found at: {csv_path}")

    df = pd.read_csv(csv_path)

    required_cols = [
        "weight",
        "steps",
        "water_intake",
        "sleep_hours",
        "risk_label",
    ]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required column(s): {missing}")

    df = df.dropna(subset=required_cols)
    if df.empty:
        raise ValueError("No data left after dropping missing rows.")

    return df


def preprocess_data(df: pd.DataFrame):
    feature_cols = ["weight", "steps", "water_intake", "sleep_hours"]
    X = df[feature_cols].astype(float)
    y_raw = df["risk_label"].astype(str)

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y_raw)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )
    return X_train, X_test, y_train, y_test, label_encoder


def train_model(X_train, y_train) -> DecisionTreeClassifier:
    model = DecisionTreeClassifier(
        criterion="gini",
        max_depth=4,
        random_state=RANDOM_STATE,
    )
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test, label_encoder: LabelEncoder):
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\nTest Accuracy: {acc:.3f}")

    y_test_labels = label_encoder.inverse_transform(y_test)
    y_pred_labels = label_encoder.inverse_transform(y_pred)
    print("\nClassification Report:")
    print(classification_report(y_test_labels, y_pred_labels))


def save_model(model, label_encoder: LabelEncoder, path: Path):
    to_save = {"model": model, "label_encoder": label_encoder}
    joblib.dump(to_save, path)
    print(f"\nModel saved to: {path}")


def main():
    print("=== Health Risk Predictor - Training Script ===")
    print(f"Loading data from: {DATA_PATH}")

    df = load_data(DATA_PATH)
    print(f"Loaded {len(df)} rows of data.")

    X_train, X_test, y_train, y_test, label_encoder = preprocess_data(df)
    print(f"Training size: {len(X_train)}, Test size: {len(X_test)}")

    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test, label_encoder)
    save_model(model, label_encoder, MODEL_PATH)


if __name__ == "__main__":
    main()
