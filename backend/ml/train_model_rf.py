from pathlib import Path
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
from sklearn.ensemble import RandomForestClassifier

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "health_data_1000.csv"
MODEL_PATH = BASE_DIR / "random_forest.pkl"

RANDOM_STATE = 42
TEST_SIZE = 0.2


def load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    required = ["weight", "height", "bmi", "steps", "water_intake", "sleep_hours", "risk_label"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df = df.dropna(subset=required)
    return df


def main():
    df = load_data()

    X = df[["weight", "height", "bmi", "steps", "water_intake", "sleep_hours"]].astype(float)
    y_raw = df["risk_label"].astype(str)

    le = LabelEncoder()
    y = le.fit_transform(y_raw)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=300,
        random_state=RANDOM_STATE,
        class_weight="balanced",
        max_depth=None,
        min_samples_leaf=5
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\n✅ Random Forest Test Accuracy: {acc:.3f}")

    print("\nClassification Report:")
    print(classification_report(le.inverse_transform(y_test), le.inverse_transform(y_pred)))

    joblib.dump({"model": model, "label_encoder": le}, MODEL_PATH)
    print(f"\n✅ Saved model: {MODEL_PATH}")


if __name__ == "__main__":
    main()
