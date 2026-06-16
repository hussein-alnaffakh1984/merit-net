"""
preprocessing.py
Reproduces the cleaned dataset (n = 1,164) from the raw Mendeley Maternal Health
Risk Assessment file (DOI 10.17632/p5w98dvbbk.1, "Dataset - Updated.csv", n = 1,205).
Cleaning = clinical validity-range filtering + missing-value removal (seed-independent).

Usage:
    python preprocessing.py --raw "Dataset - Updated.csv" --out mendeley_cleaned.csv
"""
import argparse
import pandas as pd

# Clinical validity ranges (inclusive) used for physiological-outlier removal.
RANGES = {
    "Age":         (10, 70),    # WHO antenatal guidelines
    "SystolicBP":  (60, 250),   # ACC/AHA
    "DiastolicBP": (30, 160),   # ACC/AHA
    "BS":          (2, 25),     # ADA Standards (mmol/L)
    "BodyTemp":    (95, 105),   # clinical thermoregulation (F)
    "BMI":         (10, 50),    # WHO BMI classification
    "HeartRate":   (40, 150),   # AHA cardiovascular
}
FEATURES = ["Age", "SystolicBP", "DiastolicBP", "BS", "BodyTemp", "BMI",
            "PrevComplications", "PreexistDiabetes", "GestDiabetes",
            "MentalHealth", "HeartRate"]

def clean(df):
    n0 = len(df)
    df = df.dropna(subset=FEATURES + ["RiskLevel"]).copy()       # missing-value removal
    for col, (lo, hi) in RANGES.items():
        if col in df.columns:
            df = df[(df[col] >= lo) & (df[col] <= hi)]            # range filtering
    df = df.reset_index(drop=True)
    print(f"raw={n0}  ->  cleaned={len(df)}  (removed {n0 - len(df)})")
    print(df["RiskLevel"].value_counts().to_dict())
    return df

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", required=True)
    ap.add_argument("--out", default="mendeley_cleaned.csv")
    a = ap.parse_args()
    clean(pd.read_csv(a.raw)).to_csv(a.out, index=False)
    print("written:", a.out)
