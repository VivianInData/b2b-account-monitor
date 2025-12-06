{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\froman\fcharset0 Times-Roman;}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;}
{\*\expandedcolortbl;;\cssrgb\c0\c0\c0;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs24 \cf0 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 import streamlit as st\
import pandas as pd\
\
# --- CONFIGURATION ---\
st.set_page_config(page_title="Strategic Account Intelligence", layout="wide")\
\
# --- PASSWORD PROTECTION ---\
def check_password():\
    """Returns `True` if the user had the correct password."""\
    def password_entered():\
        if st.session_state["password"] == st.secrets["password"]:\
            st.session_state["password_correct"] = True\
            del st.session_state["password"]  # Don't store password\
        else:\
            st.session_state["password_correct"] = False\
\
    if "password_correct" not in st.session_state:\
        st.text_input("Enter Access Code:", type="password", on_change=password_entered, key="password")\
        return False\
    elif not st.session_state["password_correct"]:\
        st.text_input("Enter Access Code:", type="password", on_change=password_entered, key="password")\
        st.error("\uc0\u55357 \u56853  Access Denied")\
        return False\
    else:\
        return True\
\
if check_password():\
    # --- MAIN DASHBOARD ---\
    # GENERIC TITLE (Safe for Portfolio)\
    st.title("\uc0\u55357 \u56522  Strategic Account Intelligence Monitor")\
    st.markdown("**Status:** \uc0\u55357 \u57314  Live | **Model:** Hybrid (IsoForest + XGBoost) | **AI:** GPT-4")\
    st.markdown("---")\
\
    # Load Data\
    try:\
        df = pd.read_csv("client_intelligence_data.csv")\
    except FileNotFoundError:\
        st.error("Data file not found. Ensure 'client_intelligence_data.csv' is in the repo.")\
        st.stop()\
\
    # Top Level Metrics\
    col1, col2, col3 = st.columns(3)\
    with col1:\
        st.metric("\uc0\u55357 \u57000  High Risk Accounts", f"\{len(df)\}")\
    with col2:\
        # Check for column name (Handles both old and new names)\
        vel_col = 'Rev_Velocity' if 'Rev_Velocity' in df.columns else 'Revenue_Velocity'\
        avg_drop = df[vel_col].mean()\
        st.metric("\uc0\u55357 \u56521  Avg Revenue Drop", f"\{avg_drop:.1%\}")\
    with col3:\
        st.metric("\uc0\u55358 \u56598  AI Strategies Ready", f"\{len(df)\}")\
\
    st.divider()\
\
    # The Action Feed\
    st.subheader("\uc0\u55357 \u56541  Priority Action List (Top 10)")\
\
    for index, row in df.iterrows():\
        with st.expander(f"\uc0\u55357 \u56628  \{row['Account_ID']\} | Risk Score: \{row['Risk_Probability']:.0%\}", expanded=True):\
            \
            c1, c2 = st.columns([1, 2])\
            \
            with c1:\
                # Handle velocity column name safely\
                vel_val = row.get('Rev_Velocity', row.get('Revenue_Velocity', 0))\
                st.info(f"**Velocity:** \{vel_val:.1%\}")\
                \
                # Parse the AI Text\
                narrative = str(row['AI_Narrative'])\
                \
                # Sanitize text just in case "Beacon" slipped in\
                narrative = narrative.replace("Beacon", "Our Company")\
                \
                if "EMAIL DRAFT:" in narrative:\
                    parts = narrative.split("EMAIL DRAFT:")\
                    diagnosis = parts[0].replace("DIAGNOSIS:", "").strip()\
                    email = parts[1].strip()\
                else:\
                    diagnosis = narrative\
                    email = "Draft pending..."\
                \
                st.warning(f"**\uc0\u55358 \u56800  AI Diagnosis:**\\n\\n\{diagnosis\}")\
            \
            with c2:\
                st.success(f"**\uc0\u9993 \u65039  Suggested Outreach:**\\n\\n\{email\}")\
                st.button(f"Push to CRM (\{row['Account_ID']\})", key=row['Account_ID'])}