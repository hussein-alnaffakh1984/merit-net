# R2.2 — Leakage-free re-implementation of baseline methods on the Mendeley dataset.
# Prints, for each baseline: full configuration + pooled 10-fold-CV accuracy.
# All preprocessing (scaling, SMOTE-ENN, PCA) is fitted on TRAINING folds only
# (imblearn Pipeline + cross_val_predict) => no leakage, tuning isolated from evaluation.
import glob, warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
try:
    import imblearn
except ImportError:
    import subprocess, sys
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "imbalanced-learn"])
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, f1_score, recall_score, confusion_matrix
from xgboost import XGBClassifier
from imblearn.combine import SMOTEENN
from imblearn.pipeline import Pipeline as ImbPipeline

SEED = 42

def load():
    for p in glob.glob("/kaggle/input/**/*.csv", recursive=True):
        try:
            d = pd.read_csv(p)
            if len(d) == 1164 and "RiskLevel" in d.columns:
                return d
        except Exception:
            pass
    return pd.read_csv("https://raw.githubusercontent.com/hussein-alnaffakh1984/merit-net/main/mendeley_cleaned.csv")

df = load()
F = ["Age","SystolicBP","DiastolicBP","BS","BodyTemp","BMI","PrevComplications",
     "PreexistDiabetes","GestDiabetes","MentalHealth","HeartRate"]
X = df[F].values
y = (df["RiskLevel"] == "High").astype(int).values
print("data:", X.shape, "| High:", int(y.sum()), "Low:", int((1 - y).sum()))

cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=SEED)

# report how many PCA components 95% variance keeps (fit on full standardized X, for printing only)
ncomp = PCA(n_components=0.95, random_state=SEED).fit(StandardScaler().fit_transform(X)).n_components_
print(f"PCA(95% variance) -> {ncomp} components (of {len(F)})\n")

def run(name, pipe, cfg):
    pred = cross_val_predict(pipe, X, y, cv=cv, n_jobs=-1)
    acc = accuracy_score(y, pred) * 100
    f1  = f1_score(y, pred) * 100
    rec = recall_score(y, pred) * 100
    tn, fp, fn, tp = confusion_matrix(y, pred).ravel()
    print(f"==== {name} ====")
    for k, v in cfg.items():
        print(f"   {k}: {v}")
    print(f"   >> Accuracy={acc:.2f}  HighRecall={rec:.2f}  F1(High)={f1:.2f}  CM[tn,fp,fn,tp]=[{tn},{fp},{fn},{tp}]\n")

# 1) Random Forest baseline
run("Random Forest (baseline)",
    ImbPipeline([("sc", StandardScaler()),
                 ("clf", RandomForestClassifier(n_estimators=300, random_state=SEED, n_jobs=-1))]),
    {"preprocessing":"StandardScaler", "resampling":"none", "dim_reduction":"none",
     "classifier":"RandomForest(n_estimators=300)", "seed":SEED,
     "cv":"10-fold stratified, nested (fit on train folds only)"})

# 2) XGBoost baseline
run("XGBoost (baseline)",
    ImbPipeline([("sc", StandardScaler()),
                 ("clf", XGBClassifier(n_estimators=300, max_depth=6, learning_rate=0.1,
                                       random_state=SEED, eval_metric="logloss", verbosity=0))]),
    {"preprocessing":"StandardScaler", "resampling":"none", "dim_reduction":"none",
     "classifier":"XGBoost(n_estimators=300, max_depth=6, lr=0.1)", "seed":SEED,
     "cv":"10-fold stratified, nested"})

# 3) Jamel et al. (2024): PCA + TreeNet (soft-voting of one tree model + one DL model)
run("Jamel (2024): PCA + TreeNet voting",
    ImbPipeline([("sc", StandardScaler()),
                 ("pca", PCA(n_components=0.95, random_state=SEED)),
                 ("clf", VotingClassifier(estimators=[
                     ("gb",  GradientBoostingClassifier(random_state=SEED)),
                     ("mlp", MLPClassifier(hidden_layer_sizes=(64,32), max_iter=500, random_state=SEED))],
                     voting="soft"))]),
    {"preprocessing":"StandardScaler", "resampling":"none",
     "dim_reduction":f"PCA(95% variance -> {ncomp} comps)",
     "classifier":"soft-voting(GradientBoosting + MLP[64,32])  [TreeNet reconstruction]",
     "seed":SEED, "cv":"10-fold stratified, nested (PCA fit on train folds only)"})

# 4) Sarker et al. (2025): SMOTE-ENN + PCA + XGBoost
run("Sarker (2025): SMOTE-ENN + PCA + XGBoost",
    ImbPipeline([("sc", StandardScaler()),
                 ("smote", SMOTEENN(random_state=SEED)),
                 ("pca", PCA(n_components=0.95, random_state=SEED)),
                 ("clf", XGBClassifier(n_estimators=300, max_depth=6, learning_rate=0.1,
                                       random_state=SEED, eval_metric="logloss", verbosity=0))]),
    {"preprocessing":"StandardScaler", "resampling":"SMOTE-ENN(random_state=42, library defaults)",
     "dim_reduction":f"PCA(95% variance -> {ncomp} comps)",
     "classifier":"XGBoost(n_estimators=300, max_depth=6, lr=0.1)",
     "seed":SEED, "cv":"10-fold stratified, nested (resampling + PCA fit on train folds only)"})

print("DONE — paste this whole output back.")
