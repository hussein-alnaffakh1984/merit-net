# MERIT-Net: Maternal Health Risk Prediction

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

An integrated machine learning pipeline for maternal health risk prediction, combining three complementary components to support nursing decision-making.

## 🌐 Live Demo

Interactive web application: **[https://merit-net.netlify.app](https://merit-net.netlify.app)** *(deploy your own copy via Netlify)*

## 📋 Overview

**MERIT-Net** (Maternal Explainable Risk Intelligent Tool — Network) combines:

1. **Clinical-Validated Outlier Removal** — Systematic identification of physiologically implausible records using clinical guideline ranges
2. **Confidence-Aware Trust Score** — Per-prediction reliability indicators integrating ensemble agreement, confidence, and stability
3. **Cost-Sensitive Classification** — 5:1 weighting reflecting the asymmetric clinical cost of false negatives

## 📊 Results

| Metric | Value | 95% CI |
|--------|-------|--------|
| Accuracy | 99.31% | [98.93%, 99.70%] |
| AUC | 0.9998 | [0.9996, 1.0000] |
| High-Risk Recall | 99.57% | [98.92%, 100.00%] |
| High-Risk Precision | 98.75% | [97.70%, 99.80%] |
| Brier Score | 0.0072 | [0.0045, 0.0100] |
| Trust Score Gap | 18.1 pp | (correct vs incorrect) |

## 📦 Dataset

- **Source**: Mendeley Maternal Health Risk Assessment Dataset
- **Citation**: Mojumdar et al. (2025), *Data in Brief* 59:111363
- **DOI**: [10.17632/p5w98dvbbk.1](https://doi.org/10.17632/p5w98dvbbk.1)
- **Records**: 1,164 (after clinical outlier removal)
- **Features**: 11 clinical features

## 🚀 Quick Start

```bash
git clone https://github.com/[username]/merit-net.git
cd merit-net
pip install -r requirements.txt
python merit_net.py
```

## 📁 Project Structure

```
merit-net/
├── index.html             # Web application
├── style.css              # Web styling
├── app.js                 # Browser prediction logic
├── model.json             # Trained model for browser
├── merit_net.py           # Python pipeline
├── requirements.txt
├── data/
│   └── mendeley_cleaned.csv
├── figures/
└── README.md
```

## 🔬 Methodology

### Component 1: Clinical Validity Ranges

| Feature | Valid Range |
|---------|-------------|
| Age | 10–70 years |
| Systolic BP | 60–250 mmHg |
| Diastolic BP | 30–160 mmHg |
| Blood Sugar | 2–25 mmol/L |
| Body Temp | 95–105 °F |
| BMI | 10–50 kg/m² |
| Heart Rate | 40–150 bpm |

### Component 2: Trust Score
```
T(x) = (0.4 × Agreement + 0.4 × Confidence + 0.2 × Stability) × 100
```

### Component 3: Cost-Sensitive Learning
5:1 weighting (high-risk : low-risk) reflecting clinical priority.

## 🏥 Clinical Applications

- **Antenatal Triage** — Rapid risk stratification
- **Community Midwifery** — Referral decision support
- **Patient Education** — Interpretable risk communication
- **Bedside Reassessment** — Real-time monitoring

## 📜 Citation

```bibtex
@article{naffakh2025meritnet,
  title={MERIT-Net: An Integrated Pipeline for Maternal Health Risk
         Prediction Combining Clinical Data Validation, Confidence-Aware
         Ensemble Learning, and Cost-Sensitive Classification},
  author={Al-Naffakh, Hussein Ali Hussein and others},
  year={2025}
}
```

## 👤 Author

**Hussein Ali Hussein Al-Naffakh**
Department of Maternal and Neonatal Health Nursing
Iraq

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

## ⚠️ Disclaimer

This software is for **research purposes only**. It is NOT intended for clinical decision-making without proper validation and supervision by qualified healthcare professionals.

## 🙏 Acknowledgments

We thank Mojumdar et al. (2025) for the public release of the Mendeley Maternal Health Risk Assessment dataset.
