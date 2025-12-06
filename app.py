import streamlit as st
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="Strategic Account Intelligence", layout="wide")

# --- PASSWORD PROTECTION ---
def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Enter Access Code:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Enter Access Code:", type="password", on_change=password_entered, key="password")
        st.error("😕 Access Denied")
        return False
    else:
        return True

if check_password():
    # --- MAIN DASHBOARD ---
    st.title("📊 Strategic Account Intelligence Monitor")
    st.markdown("**Status:** 🟢 Live | **Model:** Hybrid (IsoForest + XGBoost) | **AI:** GPT-4")
    st.info("This is a demo environment using anonymized B2B transaction data.")
    st.markdown("---")

    # Load Data
    try:
        df = pd.read_csv("client_intelligence_data.csv")
    except FileNotFoundError:
        st.error("Data file not found. Please ensure 'client_intelligence_data.csv' is in the repo.")
        st.stop()

    # Metrics Row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🚨 High Risk Accounts", f"{len(df)}")
    with col2:
        avg_risk = df['Risk_Probability'].mean()
        st.metric("🔥 Avg Risk Score", f"{avg_risk:.0%}")
    with col3:
        # Check for column name
        velocity_col = 'Rev_Velocity' if 'Rev_Velocity' in df.columns else 'Revenue_Velocity'
        avg_vel = df[velocity_col].mean()
        st.metric("📉 Avg Revenue Velocity", f"{avg_vel:.1%}")

    st.markdown("### 📝 Priority Action List (Top 10)")

    # Display Accounts
    for index, row in df.iterrows():
        with st.expander(f"🔴 {row['Account_ID']} | Risk: {row['Risk_Probability']:.0%}", expanded=True):
            c1, c2 = st.columns([1, 2])
            
            with c1:
                # Handle velocity column name safely
                velocity_val = row.get('Rev_Velocity', row.get('Revenue_Velocity', 0))
                st.info(f"**Velocity Shift:** {velocity_val:.1%}")
                
                # Parse the AI Text
                narrative = str(row['AI_Narrative'])
                narrative = narrative.replace("Beacon", "Our Company")
                
                if "EMAIL DRAFT:" in narrative:
                    parts = narrative.split("EMAIL DRAFT:")
                    diagnosis = parts[0].replace("DIAGNOSIS:", "").strip()
                    email = parts[1].strip()
                else:
                    diagnosis = narrative
                    email = "Draft pending..."
                
                st.warning(f"**🧠 AI Diagnosis:**\n\n{diagnosis}")
            
            with c2:
                st.success(f"**✉️ Suggested Outreach:**\n\n{email}")
                st.button(f"Push to CRM ({row['Account_ID']})", key=row['Account_ID'])
