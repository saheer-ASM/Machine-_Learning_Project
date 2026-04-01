import streamlit as st
import pandas as pd
import numpy as np
import pickle

# ── Page Config ──
st.set_page_config(
    page_title="NexaBank | Credit Approval",
    page_icon="🏦",
    layout="wide"
)

# ── Custom CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0f1e;
    color: #e8eaf0;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem !important; max-width: 100% !important; }

.bank-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(0,163,255,0.1);
    border: 1px solid rgba(0,163,255,0.25);
    border-radius: 30px;
    padding: 6px 18px;
    font-size: 12px;
    font-weight: 500;
    color: #00a3ff;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 20px;
}
.bank-name {
    font-family: 'Playfair Display', serif;
    font-size: 72px;
    font-weight: 700;
    background: linear-gradient(135deg, #ffffff 0%, #a8c8ff 50%, #00d4b4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 12px;
}
.bank-tagline {
    font-size: 18px;
    color: #8892a4;
    font-weight: 300;
    margin-bottom: 8px;
}
.bank-divider {
    width: 60px;
    height: 3px;
    background: linear-gradient(90deg, #00a3ff, #00d4b4);
    margin: 24px 0 36px;
    border-radius: 2px;
}
.feature-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 22px 18px;
    text-align: center;
    margin-bottom: 16px;
}
.feature-icon { font-size: 28px; margin-bottom: 10px; }
.feature-label { font-size: 13px; color: #8892a4; font-weight: 500; }

.section-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #00a3ff;
    margin: 28px 0 16px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(0,163,255,0.2);
}
.form-title {
    font-family: 'Playfair Display', serif;
    font-size: 34px;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 6px;
}
.form-subtitle { font-size: 14px; color: #8892a4; margin-bottom: 24px; }

.result-approved {
    background: linear-gradient(135deg, rgba(0,212,130,0.1), rgba(0,212,130,0.03));
    border: 1px solid rgba(0,212,130,0.3);
    border-radius: 16px;
    padding: 36px;
    text-align: center;
    margin-top: 20px;
}
.result-rejected {
    background: linear-gradient(135deg, rgba(255,75,75,0.1), rgba(255,75,75,0.03));
    border: 1px solid rgba(255,75,75,0.3);
    border-radius: 16px;
    padding: 36px;
    text-align: center;
    margin-top: 20px;
}
.result-icon { font-size: 56px; margin-bottom: 14px; }
.result-title-a { font-family: 'Playfair Display', serif; font-size: 30px; font-weight: 700; color: #00d482; margin-bottom: 8px; }
.result-title-r { font-family: 'Playfair Display', serif; font-size: 30px; font-weight: 700; color: #ff4b4b; margin-bottom: 8px; }
.result-prob { font-size: 15px; color: #8892a4; margin-bottom: 18px; }
.ref-tag {
    display: inline-block;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 8px;
    padding: 7px 18px;
    font-size: 12px;
    color: #8892a4;
    margin-top: 16px;
    letter-spacing: 1px;
}

/* Widget styling */
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stNumberInput"] > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e8eaf0 !important;
}
label[data-testid="stWidgetLabel"] p {
    color: #b0b8c8 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #0066cc, #00a3ff) !important;
    border: none !important;
    border-radius: 12px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    padding: 14px !important;
    letter-spacing: 0.5px !important;
    transition: all 0.3s ease !important;
}
div[data-testid="stButton"] > button[kind="secondary"] {
    background: transparent !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: #8892a4 !important;
    font-size: 13px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session State ──
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

# ════════════════════════════════════
# LANDING PAGE
# ════════════════════════════════════
if st.session_state.page == 'landing':

    st.markdown('<br><br>', unsafe_allow_html=True)
    st.markdown('<div class="bank-badge">🏦 &nbsp; Trusted Financial Services</div>', unsafe_allow_html=True)
    st.markdown('<div class="bank-name">NexaBank</div>', unsafe_allow_html=True)
    st.markdown('<div class="bank-tagline">Intelligent Credit Solutions for the Modern World</div>', unsafe_allow_html=True)
    st.markdown('<div class="bank-tagline" style="font-size:15px">Powered by Machine Learning — Fast, Fair, Accurate.</div>', unsafe_allow_html=True)
    st.markdown('<div class="bank-divider"></div>', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)

    btn_col1, btn_col2 = st.columns([1.5, 2.5])
    with btn_col1:
        if st.button("Check Credit Card Approval  →", type="primary", use_container_width=True):
            st.session_state.page = 'form'
            st.rerun()

    st.markdown('<br><br>', unsafe_allow_html=True)

# ════════════════════════════════════
# FORM PAGE
# ════════════════════════════════════
elif st.session_state.page == 'form':

    @st.cache_resource
    def load_model():
        model = pickle.load(open("model.pkl", "rb"))
        scaler = pickle.load(open("scaler.pkl", "rb"))
        columns = pickle.load(open("columns.pkl", "rb"))
        return model, scaler, columns

    model, scaler, columns = load_model()

    # Top bar
    top1, top2 = st.columns([3, 1])
    with top1:
        st.markdown('<div style="font-family:\'Playfair Display\',serif; font-size:20px; font-weight:700; background:linear-gradient(135deg,#fff,#00a3ff); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;">🏦 NexaBank</div>', unsafe_allow_html=True)
    with top2:
        if st.button("← Back to Home", type="secondary"):
            st.session_state.page = 'landing'
            st.rerun()

    st.markdown("---")
    st.markdown('<div class="form-title">Credit Card Application Form</div>', unsafe_allow_html=True)
    st.markdown('<div class="form-subtitle">Please complete all sections accurately. The AI system will evaluate the application instantly.</div>', unsafe_allow_html=True)

    # ── Personal Information ──
    st.markdown('<div class="section-label">01 &nbsp; Personal Information</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: gender = st.selectbox("Gender", ["Male (1)", "Female (0)"])
    with c2: age = st.number_input("Age (years)", min_value=18.0, max_value=100.0, value=30.0, step=0.1)
    with c3: married = st.selectbox("Marital Status", ["Married (1)", "Not Married (0)"])
    with c4: drivers_license = st.selectbox("Drivers License", ["Yes (1)", "No (0)"])

    c5, c6, c7 = st.columns(3)
    with c5: ethnicity = st.selectbox("Ethnicity", ["White", "Black", "Asian", "Latino", "Other"])
    with c6: citizen = st.selectbox("Citizenship Status", ["ByBirth", "ByOtherMeans", "Temporary"])
    with c7: zip_code = st.number_input("Zip Code", min_value=0, value=200, step=1)

    # ── Employment & Financial ──
    st.markdown('<div class="section-label">02 &nbsp; Employment & Financial Information</div>', unsafe_allow_html=True)
    c8, c9, c10 = st.columns(3)
    with c8: employed = st.selectbox("Currently Employed", ["Yes (1)", "No (0)"])
    with c9: years_employed = st.number_input("Years Employed", min_value=0.0, value=1.0, step=0.1)
    with c10: industry = st.selectbox("Industry Sector", [
        "Industrials", "Materials", "CommunicationServices", "Transport",
        "InformationTechnology", "Financials", "Energy", "Real Estate",
        "Utilities", "ConsumerDiscretionary", "Education",
        "ConsumerStaples", "Healthcare", "Research"
    ])

    c11, c12, c13 = st.columns(3)
    with c11: income = st.number_input("Annual Income ($)", min_value=0.0, value=0.0, step=100.0)
    with c12: debt = st.number_input("Current Debt ($)", min_value=0.0, value=0.0, step=0.01)
    with c13: credit_score = st.number_input("Credit Score", min_value=0, value=0, step=1)

    # ── Banking Details ──
    st.markdown('<div class="section-label">03 &nbsp; Banking Information</div>', unsafe_allow_html=True)
    c14, c15, c16 = st.columns(3)
    with c14: bank_customer = st.selectbox("Existing Bank Customer", ["Yes (1)", "No (0)"])
    with c15: prior_default = st.selectbox("Prior Default History", ["Yes (1)", "No (0)"])
    with c16: st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("---")

    # ── Submit ──
    b1, b2, b3 = st.columns([1.5, 2, 1.5])
    with b2:
        submitted = st.button("🔍  Submit Application for Review", type="primary", use_container_width=True)

    # ── Process & Show Result ──
    if submitted:
        input_dict = {col: 0 for col in columns}
        input_dict['Age'] = age
        input_dict['Debt'] = debt
        input_dict['YearsEmployed'] = years_employed
        input_dict['CreditScore'] = credit_score
        input_dict['ZipCode'] = zip_code
        input_dict['Income'] = income
        input_dict['Gender'] = 1 if "1" in gender else 0
        input_dict['Married'] = 1 if "1" in married else 0
        input_dict['BankCustomer'] = 1 if "1" in bank_customer else 0
        input_dict['PriorDefault'] = 1 if "1" in prior_default else 0
        input_dict['Employed'] = 1 if "1" in employed else 0
        input_dict['DriversLicense'] = 1 if "1" in drivers_license else 0

        def set_one_hot(prefix, value):
            col_name = f"{prefix}_{value}"
            if col_name in input_dict:
                input_dict[col_name] = 1

        set_one_hot("Industry", industry)
        set_one_hot("Ethnicity", ethnicity)
        set_one_hot("Citizen", citizen)

        input_df = pd.DataFrame([input_dict])
        proba = model.predict_proba(input_df)[0][1]
        approved = proba >= 0.5

        import random
        ref = f"NXB-{random.randint(100000, 999999)}"

        r1, r2, r3 = st.columns([1, 2, 1])
        with r2:
            if approved:
                st.markdown(f"""
                <div class="result-approved">
                    <div class="result-icon">✅</div>
                    <div class="result-title-a">Application Approved</div>
                    <div class="result-prob">
                        Approval Confidence: <strong style="color:#00d482; font-size:18px">{proba:.1%}</strong>
                    </div>
                    <div style="background:rgba(255,255,255,0.06);border-radius:100px;height:8px;overflow:hidden;max-width:280px;margin:0 auto 8px;">
                        <div style="height:100%;width:{proba*100:.1f}%;background:linear-gradient(90deg,#00a3ff,#00d482);border-radius:100px;"></div>
                    </div>
                    <div class="ref-tag">Reference No: {ref}</div>
                </div>
                """, unsafe_allow_html=True)
                
            else:
                st.markdown(f"""
                <div class="result-rejected">
                    <div class="result-icon">❌</div>
                    <div class="result-title-r">Application Declined</div>
                    <div class="result-prob">
                        Approval Confidence: <strong style="color:#ff4b4b; font-size:18px">{proba:.1%}</strong>
                    </div>
                    <div style="background:rgba(255,255,255,0.06);border-radius:100px;height:8px;overflow:hidden;max-width:280px;margin:0 auto 8px;">
                        <div style="height:100%;width:{proba*100:.1f}%;background:linear-gradient(90deg,#ff8c42,#ff4b4b);border-radius:100px;"></div>
                    </div>
                    <div class="ref-tag">Reference No: {ref}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("📋 View Full Application Summary"):
            summary = {
                "Field": ["Age", "Gender", "Marital Status", "Employed", "Years Employed",
                          "Industry", "Annual Income", "Current Debt", "Credit Score",
                          "Bank Customer", "Prior Default", "Ethnicity", "Citizenship", "Zip Code"],
                "Value": [
                    f"{age} years",
                    "Male" if "1" in gender else "Female",
                    "Married" if "1" in married else "Not Married",
                    "Yes" if "1" in employed else "No",
                    f"{years_employed} years",
                    industry, f"${income:,.0f}", f"${debt:.2f}",
                    credit_score,
                    "Yes" if "1" in bank_customer else "No",
                    "Yes" if "1" in prior_default else "No",
                    ethnicity, citizen, zip_code
                ]
            }
            st.dataframe(pd.DataFrame(summary), use_container_width=True, hide_index=True)