"""
MERIT-Net v9: Integrated Pipeline for Maternal Health Risk Prediction
Components:
1. Clinical-Validated Outlier Removal
2. Confidence-Aware Trust Score
3. Cost-Sensitive Class Weighting (5:1)
"""

import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.metrics import (accuracy_score, f1_score, roc_auc_score,
                             precision_score, recall_score, brier_score_loss)
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier

SEED = 42
COST_RATIO = 5
N_FOLDS = 10

CLINICAL_RANGES = {
    "Age": (10, 70),
    "SystolicBP": (60, 250),
    "DiastolicBP": (30, 160),
    "BS": (2, 25),
    "BodyTemp": (95, 105),
    "BMI": (10, 50),
    "HeartRate": (40, 150)
}

def clinical_outlier_removal(df):
    """Remove records with implausible values."""
    initial = len(df)
    for feat, (lo, hi) in CLINICAL_RANGES.items():
        if feat in df.columns:
            df = df[(df[feat] >= lo) & (df[feat] <= hi)]
    df = df.dropna().reset_index(drop=True)
    print(f"Removed {initial - len(df)} records")
    return df

def compute_trust_score(all_probs):
    """Trust Score = 0.4*Agreement + 0.4*Confidence + 0.2*Stability"""
    predictions = np.argmax(all_probs, axis=2)
    n_models = all_probs.shape[0]
    n_samples = all_probs.shape[1]
    agreements = []
    for i in range(n_samples):
        sample_preds = predictions[:, i]
        unique, counts = np.unique(sample_preds, return_counts=True)
        agreements.append(counts.max() / n_models)
    agreements = np.array(agreements)
    mean_probs = all_probs.mean(axis=0)
    confidence = mean_probs.max(axis=1)
    var_probs = all_probs.std(axis=0)
    variance_norm = 1 - var_probs.max(axis=1)
    return (0.4 * agreements + 0.4 * confidence + 0.2 * variance_norm) * 100

def build_merit_net(class_weights):
    """5 base learners with cost-sensitive weights."""
    return [
        RandomForestClassifier(n_estimators=500, max_depth=20,
                              class_weight=class_weights,
                              random_state=SEED, n_jobs=-1),
        XGBClassifier(n_estimators=500, max_depth=10, learning_rate=0.05,
                     scale_pos_weight=COST_RATIO, random_state=SEED,
                     eval_metric="logloss", n_jobs=-1, verbosity=0),
        CatBoostClassifier(iterations=500, depth=12, learning_rate=0.05,
                          class_weights=[1.0, COST_RATIO],
                          random_seed=SEED, verbose=0),
        LGBMClassifier(n_estimators=500, max_depth=10, learning_rate=0.05,
                      class_weight=class_weights, random_state=SEED,
                      n_jobs=-1, verbose=-1),
        ExtraTreesClassifier(n_estimators=500, max_depth=20,
                            class_weight=class_weights,
                            random_state=SEED, n_jobs=-1)
    ]

def evaluate(X, y, class_weights):
    """10-fold stratified CV."""
    skf = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)
    metrics = {"accuracy": [], "auc": [], "hr_recall": [], "brier": []}
    trust_scores = {"correct": [], "wrong": []}
    for fold, (tr, te) in enumerate(skf.split(X, y)):
        X_tr, X_te = X[tr], X[te]
        y_tr, y_te = y[tr], y[te]
        models = build_merit_net(class_weights)
        for m in models:
            m.fit(X_tr, y_tr)
        all_probs = np.array([m.predict_proba(X_te) for m in models])
        p_ens = all_probs.mean(axis=0)
        preds = p_ens.argmax(1)
        proba = p_ens[:, 1]
        ts = compute_trust_score(all_probs)
        trust_scores["correct"].extend(ts[preds == y_te].tolist())
        trust_scores["wrong"].extend(ts[preds != y_te].tolist())
        metrics["accuracy"].append(accuracy_score(y_te, preds))
        metrics["auc"].append(roc_auc_score(y_te, proba))
        metrics["hr_recall"].append(recall_score(y_te, preds))
        metrics["brier"].append(brier_score_loss(y_te, proba))
        print(f"Fold {fold+1}: Acc={metrics['accuracy'][-1]:.4f}")
    return metrics, trust_scores

if __name__ == "__main__":
    df = pd.read_csv("data/mendeley_cleaned.csv")
    features = ["Age", "SystolicBP", "DiastolicBP", "BS", "BodyTemp",
                "BMI", "PrevComplications", "PreexistDiabetes",
                "GestDiabetes", "MentalHealth", "HeartRate"]
    X = df[features].values
    y = (df["RiskLevel"] == "High").astype(int).values
    class_weights = {0: 1.0, 1: float(COST_RATIO)}
    metrics, trust_scores = evaluate(X, y, class_weights)
    print(f"Final Accuracy: {np.mean(metrics['accuracy'])*100:.2f}%")
    print(f"HR Recall: {np.mean(metrics['hr_recall'])*100:.2f}%")