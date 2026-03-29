import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load model files
model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))

# Page config
st.set_page_config(page_title="Credit Card Approval", page_icon="💳", layout="centered")

st.title("💳 Credit Card Approval Prediction")
st.markdown("---")
st.write("Fill in the applicant details below and click **Predict** to get the result.")

# ── INPUT SECTION ──
col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox("Gender", ["Male (1)", "Female (0)"])
    age = st.number_input("Age", min_value=18.0, max_value=100.0, value=30.0, step=0.1)
    debt = st.number_input("Debt", min_value=0.0, value=0.0, step=0.01)
    married = st.selectbox("Married", ["Yes (1)", "No (0)"])
    bank_customer = st.selectbox("Bank Customer", ["Yes (1)", "No (0)"])
    industry = st.selectbox("Industry", [
        "Industrials", "Materials", "CommunicationServices",
        "Transport", "InformationTechnology", "Financials",
        "Energy", "Real Estate", "Utilities",
        "ConsumerDiscretionary", "Education", "ConsumerStaples",
        "Healthcare", "Research"
    ])
    ethnicity = st.selectbox("Ethnicity", ["White", "Black", "Asian", "Latino", "Other"])

with col2:
    years_employed = st.number_input("Years Employed", min_value=0.0, value=1.0, step=0.1)
    prior_default = st.selectbox("Prior Default", ["Yes (1)", "No (0)"])
    employed = st.selectbox("Currently Employed", ["Yes (1)", "No (0)"])
    credit_score = st.number_input("Credit Score", min_value=0, value=0, step=1)
    drivers_license = st.selectbox("Drivers License", ["Yes (1)", "No (0)"])
    citizen = st.selectbox("Citizen", ["ByBirth", "ByOtherMeans", "Temporary"])
    zip_code = st.number_input("Zip Code", min_value=0, value=200, step=1)
    income = st.number_input("Income", min_value=0.0, value=0.0, step=1.0)

st.markdown("---")

# ── BUILD INPUT ──
input_dict = {col: 0 for col in columns}

# Numerical
input_dict['Age'] = age
input_dict['Debt'] = debt
input_dict['YearsEmployed'] = years_employed
input_dict['CreditScore'] = credit_score
input_dict['ZipCode'] = zip_code
input_dict['Income'] = income

# Binary
input_dict['Gender'] = 1 if "1" in gender else 0
input_dict['Married'] = 1 if "1" in married else 0
input_dict['BankCustomer'] = 1 if "1" in bank_customer else 0
input_dict['PriorDefault'] = 1 if "1" in prior_default else 0
input_dict['Employed'] = 1 if "1" in employed else 0
input_dict['DriversLicense'] = 1 if "1" in drivers_license else 0

# One-hot
def set_one_hot(prefix, value):
    col_name = f"{prefix}_{value}"
    if col_name in input_dict:
        input_dict[col_name] = 1

set_one_hot("Industry", industry)
set_one_hot("Ethnicity", ethnicity)
set_one_hot("Citizen", citizen)

# ── PREDICT ──
if st.button("Predict", use_container_width=True):
    input_df = pd.DataFrame([input_dict])

    # RF uses unscaled data
    proba = model.predict_proba(input_df)[0][1]

    st.markdown("---")
    st.subheader("Prediction Result")
    st.write(f"**Approval Probability: {proba:.2%}**")

    st.progress(float(proba))

    if proba >= 0.5:
        st.success("Credit Card APPROVED")
        st.balloons()
    else:
        st.error("Credit Card REJECTED")

    with st.expander("View Input Summary"):
        summary = {
            "Age": age, "Debt": debt, "Income": income,
            "Years Employed": years_employed, "Credit Score": credit_score,
            "Industry": industry, "Ethnicity": ethnicity, "Citizen": citizen
        }
        st.table(pd.DataFrame([summary]).T.rename(columns={0: "Value"}))