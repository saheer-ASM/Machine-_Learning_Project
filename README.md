# Credit Card Approval Prediction 

A Streamlit web app that predicts whether a credit application is likely to be approved based on applicant and banking attributes. The UI is implemented in `app.py` (NexaBank-themed), and the underlying model is trained in `Model.ipynb` and serialized to `model.pkl`.

## What's included

- Streamlit app: interactive application form + approval probability
- Training notebook: preprocessing, model training, evaluation, and artifact export
- Artifacts used by the app: `model.pkl`, `columns.pkl` (feature schema), `scaler.pkl` (saved from notebook)

## Dataset

- File: `dataset.csv`
- Shape: **690 rows x 16 columns** (includes target column `Approved`)
- Training notebook uses **688 rows** after dropping 2 rows with missing `Income`
- Preprocessing in `Model.ipynb`:
  - Fill missing `Age` with the median
  - Fill missing `Married` and `Employed` with the mode
  - One-hot encode `Industry`, `Ethnicity`, and `Citizen` (resulting in **34** model features)

## Model & results (from `Model.ipynb`)

Train/test split: `test_size=0.2`, `random_state=44`.

- Random Forest (`RandomForestClassifier(n_estimators=100, random_state=42)`)
  - Accuracy: **0.8986**
  - Precision: **0.8462**
  - Recall: **0.9322**
  - F1-score: **0.8871**
- SVM (baseline, trained on scaled features)
  - Accuracy: **0.8478**
  - Precision: **0.7639**
  - Recall: **0.9322**
  - F1-score: **0.8397**

The Streamlit app uses the Random Forest model. `scaler.pkl` is saved by the notebook (used for the SVM experiment) and is loaded by the app, but the Random Forest prediction path does not apply scaling.

## Run the app locally

1. Install dependencies:
   - App: `streamlit`, `pandas`, `numpy`, `scikit-learn`
2. Start the Streamlit server:

```bash
streamlit run app.py
```

Make sure `model.pkl`, `columns.pkl`, and `scaler.pkl` are present in the project root (same folder as `app.py`).

## Retrain / regenerate artifacts

Open and run `Model.ipynb`. The final cells export:

- `model.pkl` (Random Forest model)
- `scaler.pkl` (StandardScaler fitted in the notebook)
- `columns.pkl` (feature columns used during training)

## Project structure

- `app.py` - Streamlit UI and inference
- `Model.ipynb` - training + evaluation
- `dataset.csv` - dataset used by the notebook
- `model.pkl` - trained model artifact
- `columns.pkl` - training feature schema
- `scaler.pkl` - scaler saved from notebook


