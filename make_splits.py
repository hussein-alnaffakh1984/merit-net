"""
make_splits.py
Deterministically regenerates and saves the exact split indices used in the paper
(seed = 42), so reviewers can reproduce every fold and the holdout without re-running
the model. Produces cv_fold_indices.json (10 folds) and holdout_indices.json (80/20).

Usage:
    python make_splits.py --data mendeley_cleaned.csv
"""
import argparse, json
import pandas as pd
from sklearn.model_selection import StratifiedKFold, train_test_split

def main(path):
    df = pd.read_csv(path)
    y = (df["RiskLevel"].astype(str).str.lower() == "high").astype(int).values
    idx = list(range(len(df)))

    # 10-fold stratified CV (matches the main results)
    skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
    folds = [{"fold": k, "train": tr.tolist(), "test": te.tolist()}
             for k, (tr, te) in enumerate(skf.split(idx, y))]
    json.dump(folds, open("cv_fold_indices.json", "w"))

    # 80/20 stratified holdout (matches Section 4.9)
    tr, te = train_test_split(idx, test_size=0.20, stratify=y, random_state=42)
    json.dump({"train": sorted(tr), "test": sorted(te), "n_train": len(tr), "n_test": len(te)},
              open("holdout_indices.json", "w"))

    print(f"n={len(df)}  CV folds=10 (seed 42)  holdout: train={len(tr)} test={len(te)}")
    print("written: cv_fold_indices.json, holdout_indices.json")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--data", default="mendeley_cleaned.csv")
    main(ap.parse_args().data)
