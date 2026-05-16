MERIT-Net: Maternal Health Risk Prediction
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)
[![Status](https://img.shields.io/badge/status-research-orange.svg)]()
> An integrated machine learning pipeline for maternal health risk prediction supporting nursing decision-making.
🌐 Live Demo
Interactive Web Application: https://meritnet-iraq.netlify.app
The web app allows clinicians to input clinical measurements and receive risk predictions with Trust Scores for decision support.
📋 Overview
MERIT-Net (Maternal Explainable Risk Intelligent Tool — Network) integrates three complementary components:
Clinical-Validated Outlier Removal — Removes physiologically implausible records using clinical guideline ranges
Confidence-Aware Trust Score — Per-prediction reliability indicators (range: 0-100%)
Cost-Sensitive Classification — 5:1 weighting reflecting asymmetric clinical costs
📊 Performance Results
Metric	Value	95% CI
Accuracy	99.31%	[98.93%, 99.70%]
AUC (ROC)	0.9998	[0.9996, 1.0000]
High-Risk Recall	99.57%	[98.92%, 100.00%]
High-Risk Precision	98.75%	[97.70%, 99.80%]
Brier Score	0.0072	[0.0045, 0.0100]
Expected Calibration Error (ECE)	0.0235	[0.0193, 0.0277]
Trust Score Gap	18.1 pp	(correct vs incorrect predictions)
Evaluated under 10-fold stratified cross-validation on the Mendeley dataset (n=1,164).
📦 Dataset
Source: Mendeley Maternal Health Risk Assessment Dataset
Citation: Mojumdar et al. (2025), Data in Brief 59:111363
DOI: 10.17632/p5w98dvbbk.1
Records: 1,164 (after clinical outlier removal from 1,205)
Features: 11 clinical features
Target: Binary risk classification (High vs. Low)
🚀 Quick Start
Installation
```bash
# Clone the repository
git clone https://github.com/hussein-alnaffakh1984/merit-net.git
cd merit-net

# Install dependencies
pip install -r requirements.txt
```
Running the Pipeline
```bash
# Run main pipeline
python merit_net.py
```
Expected output:
```
Fold  1: Acc=0.9915 | AUC=1.0000 | HR-Rec=0.9787
...
Final Accuracy: 99.31%
HR Recall: 99.57%
```
🔬 Methodology Details
Component 1: Clinical Validity Ranges
Based on established clinical guidelines:
Feature	Valid Range	Reference
Age	10–70 years	WHO antenatal guidelines
Systolic BP	60–250 mmHg	ACC/AHA guidelines
Diastolic BP	30–160 mmHg	ACC/AHA guidelines
Blood Sugar	2–25 mmol/L	ADA Standards
Body Temp	95–105 °F	Clinical thermoregulation
BMI	10–50 kg/m²	WHO BMI classification
Heart Rate	40–150 bpm	AHA cardiovascular
Component 2: Trust Score Formula
```
T(x) = (0.4 × A(x) + 0.4 × C(x) + 0.2 × V(x)) × 100
```
Where:
A(x) = Agreement among 5 base learners (proportion ∈ [0,1])
C(x) = Mean confidence of predicted class ∈ [0,1]
V(x) = 1 − min(std(probabilities), 1) ∈ [0,1]
Component 3: Cost-Sensitive Learning
5:1 weighting ratio reflecting that missing a high-risk pregnancy is clinically far more costly than a false alarm.
📁 Project Structure
```
merit-net/
├── index.html                  # Web application
├── style.css                   # Styling
├── app.js                      # Browser-side prediction
├── model.json                  # Trained model (browser-deployable)
├── merit_net.py                # Main Python pipeline
├── requirements.txt            # Dependencies
├── netlify.toml                # Netlify config
├── README.md                   # This file
├── DEPLOYMENT.md               # Deployment guide
├── LICENSE                     # MIT License
├── data/
│   └── mendeley_cleaned.csv    # Cleaned dataset (n=1,164)
└── figures/                    # Paper figures (300 DPI)
    ├── fig0_class_distribution.png
    ├── fig1_boxplots.png
    ├── fig2_correlation.png
    ├── fig3_confusion_matrix.png
    ├── fig4_roc_curve.png
    ├── fig5_feature_importance.png
    ├── fig6_comparison.png
    └── fig7_trust_score.png
```
🔁 Reproducibility
All experiments use fixed random seeds and standardized protocols:
Random seed: 42 (NumPy, scikit-learn, XGBoost, CatBoost, LightGBM, Extra Trees)
Cross-validation: 10-fold stratified (`random_state=42`)
Software versions:
Python 3.10
NumPy v1.24
scikit-learn v1.3
XGBoost v2.0
CatBoost v1.2
LightGBM v4.0
Hardware: Kaggle Notebooks computing environment (CPU-based; tree-based ensembles do not benefit from GPU acceleration)
🏥 Clinical Applications
MERIT-Net is intended to support, not replace, nursing decision-making:
Antenatal Triage — Risk stratification for patient prioritization
Community Midwifery — Referral decision support in rural settings
Patient Education — Interpretable risk communication
Bedside Reassessment — Real-time risk monitoring
⚠️ Important Disclaimers
Research tool only: Not intended for clinical decision-making without proper validation
Single-source data: Validation on multi-center external datasets is essential before deployment
No clinician validation: Future work includes structured clinician evaluation studies
Use under supervision: All predictions must be interpreted by qualified healthcare professionals
👤 Author
Hussein Ali Hussein Al-Naffakh
Department of Maternal and Neonatal Health Nursing
Iraq
GitHub: @hussein-alnaffakh1984
📄 License
This project is licensed under the MIT License — see the LICENSE file for details.
🙏 Acknowledgments
We thank Mojumdar et al. (2025) for the public release of the Mendeley Maternal Health Risk Assessment dataset that made this research possible.
📧 Contact
For questions or collaboration: Please open an issue on this GitHub repository.
---
⭐ If you find this work useful, please consider starring the repository!
