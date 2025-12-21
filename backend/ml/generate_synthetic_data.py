from pathlib import Path
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
OUT_PATH = BASE_DIR / "health_data_1000.csv"

RANDOM_STATE = 42
N = 1000


def calc_bmi(weight_kg: float, height_cm: float) -> float:
    h_m = height_cm / 100.0
    return weight_kg / (h_m * h_m)


def risk_label_rule(bmi: float, steps: int, water: float, sleep: float) -> str:
    """
    Interpretable rule to label synthetic data.
    This defines what "Low/Medium/High" means for the dataset.
    """
    score = 0

    # BMI contribution
    if bmi >= 30:
        score += 2
    elif bmi >= 25:
        score += 1
    elif bmi < 18.5:
        score += 1

    # steps contribution
    if steps < 4000:
        score += 2
    elif steps < 7000:
        score += 1

    # water contribution
    if water < 1.5:
        score += 2
    elif water < 2.0:
        score += 1

    # sleep contribution
    if sleep < 6:
        score += 2
    elif sleep < 7:
        score += 1

    if score >= 6:
        return "High"
    elif score >= 3:
        return "Medium"
    return "Low"


def main():
    rng = np.random.default_rng(RANDOM_STATE)

    # height in cm, realistic adult range
    height_cm = rng.normal(loc=170, scale=10, size=N).clip(145, 200)

    # weight correlated with height (roughly), add noise
    base_weight = (height_cm - 100) + rng.normal(0, 12, size=N)
    weight_kg = base_weight.clip(40, 140)

    # steps: skewed distribution (some low, some high)
    steps = rng.normal(loc=7500, scale=2500, size=N).clip(500, 18000).astype(int)

    # water intake in liters/day
    water = rng.normal(loc=2.2, scale=0.7, size=N).clip(0.5, 5.0)

    # sleep hours/night
    sleep = rng.normal(loc=7.0, scale=1.2, size=N).clip(3.5, 10.5)

    bmi = np.array([calc_bmi(w, h) for w, h in zip(weight_kg, height_cm)])
    labels = [risk_label_rule(b, s, wtr, slp) for b, s, wtr, slp in zip(bmi, steps, water, sleep)]

    df = pd.DataFrame({
        "weight": np.round(weight_kg, 1),
        "height": np.round(height_cm, 1),
        "bmi": np.round(bmi, 2),
        "steps": steps,
        "water_intake": np.round(water, 2),
        "sleep_hours": np.round(sleep, 2),
        "risk_label": labels
    })

    df.to_csv(OUT_PATH, index=False)
    print(f"✅ Saved synthetic dataset: {OUT_PATH}")
    print(df["risk_label"].value_counts())


if __name__ == "__main__":
    main()
