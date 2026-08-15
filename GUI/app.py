import json
from datetime import date, time

import requests
import streamlit as st
from options_data import MERCHANTS, CATEGORIES

API_URL = "http://localhost:8000/predict"
TIMEOUT_SEC = 15

st.set_page_config(page_title="Fraud Prediction", page_icon="💳", layout="centered")

st.title("💳 Transaction Fraud Prediction")
st.caption("Fill in the transaction details and get a live prediction from the API.")

with st.form("txn_form"):
    st.subheader("Transaction Details")

    col1, col2 = st.columns(2)
    with col1:
        trans_date = st.date_input("Transaction Date", value=date(2021, 1, 1),min_value=date(1950, 1, 1),
            max_value=date.today(),)
    with col2:
        trans_time = st.time_input("Transaction Time", value=time(12, 0, 0))

    merchant = st.selectbox("Merchant", options=MERCHANTS, index=0,
                             help="Start typing to search")
    category = st.selectbox("Category", options=CATEGORIES, index=0,
                             help="Start typing to search")

    amt = st.number_input("Amount ($)", min_value=0.0, value=765.0, step=1.0, format="%.2f")

    gender = st.selectbox("Gender", options=["M", "F"], index=0)

    st.subheader("Cardholder Location")
    col3, col4 = st.columns(2)
    with col3:
        lat = st.number_input("Latitude", value=40.7128, format="%.6f")
    with col4:
        long = st.number_input("Longitude", value=-74.0060, format="%.6f")

    city_pop = st.number_input("City Population", min_value=0, value=8000000, step=1000)

    dob = st.date_input("Date of Birth", value=date(1990, 1, 1),
                         min_value=date(1900, 1, 1), max_value=date.today())

    st.subheader("Merchant Location")
    col5, col6 = st.columns(2)
    with col5:
        merch_lat = st.number_input("Merchant Latitude", value=40.7128, format="%.6f")
    with col6:
        merch_long = st.number_input("Merchant Longitude", value=-74.0060, format="%.6f")

    submitted = st.form_submit_button("🔮 Predict", use_container_width=True)

if submitted:
    trans_dt_str = f"{trans_date.strftime('%Y-%m-%d')} {trans_time.strftime('%H:%M:%S')}"

    payload = {
        "trans_date_trans_time": trans_dt_str,
        "merchant": merchant,
        "category": category,
        "amt": amt,
        "gender": gender,
        "lat": lat,
        "long": long,
        "city_pop": int(city_pop),
        "dob": dob.strftime("%Y-%m-%d"),
        "merch_lat": merch_lat,
        "merch_long": merch_long,
    }

    try:
        with st.spinner("Getting prediction..."):
            resp = requests.post(API_URL, json=payload, timeout=TIMEOUT_SEC)

        if resp.status_code != 200:
            st.error(f"API returned an error (status {resp.status_code})")
            st.code(resp.text)
        else:
            try:
                result = resp.json()
            except ValueError:
                st.error("API response is not valid JSON.")
                st.code(resp.text)
                result = None

            if result is not None:
                pred = result.get("prediction is ")
                prob = result.get("probability")

                st.divider()
                st.subheader("📊 Prediction Result")

                if pred is not None:
                    is_fraud = "fraud" in str(pred).lower() and "normal" not in str(pred).lower()
                    if is_fraud:
                        st.markdown(
                            "<div style='padding:24px;border-radius:12px;background-color:#3a1414;"
                            "border:2px solid #e03131;text-align:center;'>"
                            "<span style='font-size:42px;'>🚨</span><br>"
                            "<span style='font-size:26px;font-weight:700;color:#ff6b6b;'>FRAUD DETECTED</span>"
                            "</div>",
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            "<div style='padding:24px;border-radius:12px;background-color:#0f2f1a;"
                            "border:2px solid #2f9e44;text-align:center;'>"
                            "<span style='font-size:42px;'>✅</span><br>"
                            "<span style='font-size:26px;font-weight:700;color:#69db7c;'>NOT FRAUD</span>"
                            "</div>",
                            unsafe_allow_html=True,
                        )
                else:
                    st.warning("Could not find a prediction value in the API response.")

                st.write("")

                if prob is not None:
                    prob_val = float(prob)
                    c1, c2 = st.columns([1, 2])
                    with c1:
                        st.metric("Fraud Probability", f"{prob_val * 100:.2f}%")
                    with c2:
                        st.progress(min(max(prob_val, 0.0), 1.0))

                with st.expander("🔍 Raw API Response"):
                    st.json(result)

    except requests.exceptions.ConnectionError:
        st.error(
            f"Could not connect to the API at {API_URL}. "
            "Make sure the local server is running."
        )
    except requests.exceptions.Timeout:
        st.error("The request timed out. The server may be slow to respond.")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
else:
    st.info("Fill in the form and click 'Predict'.")