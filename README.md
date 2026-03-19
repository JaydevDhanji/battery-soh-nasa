# EV Battery State-of-Health (SoH) Estimation (NASA) — CPU + Uncertainty

This project estimates Li-ion battery State-of-Health (SoH) from a cleaned NASA battery dataset using a leakage-safe ML workflow (grouped by battery_id). It also produces calibrated uncertainty intervals using a group-bootstrapped ensemble.

## Highlights
- Robust SoH definition using baseline capacity = median of first 5 discharge cycles
- Leakage-safe evaluation with GroupKFold (grouped by battery_id)
- XGBoost model with monotonic constraint on cycle index
- Uncertainty: group-bootstrap + post-hoc calibration to target empirical coverage

## Project structure
- `src/data/` data processing + plotting
- `src/models/` training, CV, uncertainty, calibration
- `docs/` design doc
- `run_all.bat` one-command pipeline runner (Windows)

## Setup (Windows / Conda)
```bat
conda create -n batterysoh python=3.11 -y
conda activate batterysoh
pip install -U pip
pip install numpy pandas pyarrow scipy scikit-learn matplotlib tqdm xgboost joblib pillow