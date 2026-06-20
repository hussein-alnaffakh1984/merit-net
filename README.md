# MERIT-Net

Confidence-aware ensemble pipeline for maternal health risk prediction with cost-sensitive classification.

- **Paper:** International Journal of Intelligent Engineering and Systems (IJIES) — under review.
- **Dataset:** Mendeley Maternal Health Risk Assessment (DOI: 10.17632/p5w98dvbbk.1).
- **Live demo:** https://meritnet-iraq.netlify.app (predictions computed client-side from `model.json`).

## Repository contents

| File | Purpose |
| --- | --- |
| `preprocessing.py` | Deterministic cleaning of the raw Mendeley file (1,205 → 1,164). |
| `make_splits.py` | Regenerates the exact 10-fold CV indices and the 80/20 holdout indices (seed 42). |
| `merit_net.py` | Main pipeline: five-model ensemble, Trust Score, SHAP. |
| `baseline_configs.py` | Leakage-free re-implementation of the comparison baselines. |
| `config.json` | All hyperparameters, seeds, conformal split, and Trust Score weights. |
| `environment.yml` / `requirements.txt` | Pinned runtime environment. |
| `mendeley_cleaned.csv` | Cleaned dataset (n = 1,164). |
| `model.json` | Trained model (browser-deployable). |
| `cv_fold_indices.json`, `holdout_indices.json` | Exact split indices (output of `make_splits.py`). |
| `fold_predictions.csv` | Out-of-fold cross-validation predictions. |
| `*.ipynb` | Notebook reproducing the tables and figures. |
| `figures/` | Figures used in the paper (`fig1`–`fig6`). |
| `index.html`, `app.js`, `style.css`, `netlify.toml` | Live web demo. |
| `REPRODUCE.md`, `DEPLOYMENT.md`, `LICENSE` | Reproduction steps, deployment notes, license. |

## Environment

```bash
conda env create -f environment.yml && conda activate merit-net
# or: pip install -r requirements.txt
```

All randomness is fixed at `random_state = 42` across NumPy 1.24, scikit-learn 1.3, XGBoost 2.0, CatBoost 1.2, and LightGBM 4.0.

## Reproduce

```bash
python preprocessing.py --raw "Dataset - Updated.csv" --out mendeley_cleaned.csv   # 1,205 -> 1,164
python make_splits.py --data mendeley_cleaned.csv                                  # writes split-index files
python merit_net.py                                                                # Tables 2-5, confusion matrices, Trust Score
python baseline_configs.py                                                         # Table 3 baselines
```

See `REPRODUCE.md` for the full order, and `config.json` for every hyperparameter.

## Headline results (10-fold stratified CV, n = 1,164)

| Metric | Value |
| --- | --- |
| Accuracy | 99.31% |
| High-risk recall | 99.57% |
| High-risk precision | 98.72% |
| AUC (ROC) | 0.9998 |
| Trust Score AUROC | 0.9796 |

Independent holdout (n = 233): 99.14% accuracy, 100% high-risk recall (zero false negatives).

## Ensemble hyperparameters (see `config.json`)

Five-model uniform soft-voting ensemble with 5:1 cost weighting:
Random Forest (500, depth 20), XGBoost (500, depth 10, lr 0.05), CatBoost (500, depth 12, lr 0.05),
LightGBM (500, depth 10, lr 0.05), Extra Trees (500, depth 20).

## Authors

- **Hussein Ali Hussein Al Naffakh** — Department of Medical Laboratory Techniques, University of Alkafeel, Najaf, Iraq.
- **Ahmed Dheyaa Radhi** — College of Pharmacy, University of Al-Ameed, Karbala, Iraq.
- **Muntaha Abdullah Reishaan** (corresponding) — Department of Anesthesia, College of Health and Medical Technology, University of Alkafeel, Najaf, Iraq — muntaha.abd@alkafeel.edu.iq

## License

Released under the MIT License (see `LICENSE`).
