import streamlit as st
import pandas as pd
import pickle

# --- PAGE CONFIG ---
st.set_page_config(page_title="Insurance Cost Analyzer", page_icon="₹", layout="wide")

# --- LOAD MODELS ---
@st.cache_resource
def load_models():
    try:
        with open("lr_model.pkl", "rb") as f:
            lr_model = pickle.load(f)

        with open("svr_model.pkl", "rb") as f:
            svr_model = pickle.load(f)

        with open("y_scaler.pkl", "rb") as f:
            y_scaler = pickle.load(f)

        return lr_model, svr_model, y_scaler
    except:
        st.error("❌ Model files not found!")
        return None, None, None


lr_model, svr_model, y_scaler = load_models()

if lr_model is None:
    st.stop()

# --- CONSTANTS ---
USD_TO_INR = 93.13
INDIA_ADJUSTMENT = 0.25  # makes cost realistic for India

PLAN_MULTIPLIERS = {
    "Basic": 1.0,
    "Standard": 1.3,
    "Premium": 1.6
}

# --- HEADER ---
st.title("🏥 Insurance Plan Cost Analyzer")
st.write("Check your insurance premium and affordability.")

# --- INPUT SECTION ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Personal Info")
    age = st.number_input("Age", 18, 100, 25)
    sex = st.selectbox("Sex", ["male", "female"])
    bmi = st.number_input("BMI", 10.0, 50.0, 24.0)

with col2:
    st.subheader("Health")
    children = st.selectbox("Children", [0,1,2,3,4,5])
    smoker = st.radio("Smoker?", ["yes", "no"])
    region = st.selectbox("Region", ["southwest","southeast","northwest","northeast"])

with col3:
    st.subheader("Income & Plan")
    salary_type = st.radio("Salary Type", ["Monthly", "Yearly"])
    salary_input = st.number_input("Enter Salary (₹)", value=50000)

    yearly_salary = salary_input if salary_type == "Yearly" else salary_input * 12

    selected_plan = st.selectbox("Select Plan", ["Basic","Standard","Premium"])
    plan_year = st.selectbox("Duration (Years)", [1,3,5])

# Model toggle
use_lr = st.toggle("Use Linear Regression (Default: SVR)")

# --- BUTTON ---
if st.button("Generate Report", use_container_width=True):

    # --- INPUT DATA ---
    input_df = pd.DataFrame([{
        'age': age,
        'sex': sex,
        'bmi': bmi,
        'children': children,
        'smoker': smoker,
        'region': region
    }])

    # --- PREDICTION (YEARLY USD) ---
    if use_lr:
        base_usd = lr_model.predict(input_df)[0]
    else:
        pred_scaled = svr_model.predict(input_df)
        base_usd = y_scaler.inverse_transform(pred_scaled.reshape(-1,1))[0][0]

    # --- CALCULATIONS ---
    discount = 1.0 if plan_year == 1 else (0.95 if plan_year == 3 else 0.90)
    monthly_salary = yearly_salary / 12

    results = []

    for plan, mult in PLAN_MULTIPLIERS.items():

        yearly_cost = base_usd * mult * USD_TO_INR * INDIA_ADJUSTMENT * discount
        yearly_cost = min(yearly_cost, 800000)  # safety cap

        monthly_cost = yearly_cost / 12
        total_cost = yearly_cost * plan_year

        percent = (monthly_cost / monthly_salary) * 100 if monthly_salary > 0 else 0

        results.append({
            "Plan": plan,
            "Monthly Payment (₹)": monthly_cost,
            "Yearly Payment (₹)": yearly_cost,
            "Total Cost (₹)": total_cost,
            "Salary Usage (%)": percent
        })

    df_result = pd.DataFrame(results)

    # --- TABLE ---
    st.subheader("📊 Cost Breakdown")
    st.dataframe(
        df_result.style.format({
            "Monthly Payment (₹)": "₹{:,.0f}",
            "Yearly Payment (₹)": "₹{:,.0f}",
            "Total Cost (₹)": "₹{:,.0f}",
            "Salary Usage (%)": "{:.1f}%"
        })
    )

    # --- SELECTED PLAN ---
    row = df_result[df_result["Plan"] == selected_plan].iloc[0]

    st.subheader("💡 Your Selected Plan")
    st.write(f"Monthly: ₹{row['Monthly Payment (₹)']:,.0f}")
    st.write(f"Yearly: ₹{row['Yearly Payment (₹)']:,.0f}")
    st.write(f"Total ({plan_year} yrs): ₹{row['Total Cost (₹)']:,.0f}")
    st.write(f"Salary Usage: {row['Salary Usage (%)']:.1f}%")

    # --- AFFORDABILITY ---
    if row["Salary Usage (%)"] > 40:
        st.error("🚨 Not affordable")
    elif row["Salary Usage (%)"] > 25:
        st.warning("⚠️ Slightly expensive")
    else:
        st.success("✅ Affordable")

    # --- SMART RECOMMENDATION ---
    st.subheader("🤖 Recommended Plan For You")

    sorted_df = df_result.sort_values("Salary Usage (%)")

    best_row = None
    for _, r in sorted_df.iterrows():
        if r["Salary Usage (%)"] <= 30:
            best_row = r
            break

    if best_row is None:
        best_row = sorted_df.iloc[0]

    recommended_plan = best_row["Plan"]

    st.markdown(f"### 🏆 Recommended Plan: **{recommended_plan}**")

    st.write(f"""
    💸 Monthly: ₹{best_row['Monthly Payment (₹)']:,.0f}  
    📅 Yearly: ₹{best_row['Yearly Payment (₹)']:,.0f}  
    📊 Salary Usage: {best_row['Salary Usage (%)']:.1f}%  
    """)

    # --- REASON ---
    if best_row["Salary Usage (%)"] <= 15:
        st.success("You can easily afford this plan with full benefits.")
    elif best_row["Salary Usage (%)"] <= 30:
        st.info("Balanced plan — good coverage at reasonable cost.")
    else:
        st.warning("This is the safest option based on your income.")

    # --- RISK ---
    st.subheader("🧠 Risk Insight")
    if smoker == "yes" or bmi > 30:
        st.error("High risk → higher premium expected")
    else:
        st.success("Normal risk profile")

    # --- CHART ---
    st.subheader("📈 Monthly Payment Comparison")
    st.bar_chart(df_result.set_index("Plan")["Monthly Payment (₹)"])