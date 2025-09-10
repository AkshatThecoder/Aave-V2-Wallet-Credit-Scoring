import streamlit as st
import pandas as pd
import sys
import os
import json

# Add the src directory to the Python path to make imports work in deployment
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from features import compute_features
from score_wallets import load_data, score

st.title("Aave V2 Wallet Credit Scoring")

st.write("""
This application assigns a credit score (0–1000) to each wallet based on their historical transaction behavior with the Aave V2 DeFi protocol.
""")

# Define a data directory within the credit-scoring-aave folder
# This helps in environments like Streamlit Cloud where the root might be different
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

uploaded_file = st.file_uploader("Choose a transactions.json file", type="json")

if uploaded_file is not None:
    # Save the uploaded file to a temporary location
    temp_file_path = os.path.join(DATA_DIR, "uploaded_transactions.json")
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"File uploaded and saved to {temp_file_path}")

    if st.button("Calculate Credit Scores"):
        try:
            with st.spinner('Loading data...'):
                # Now we can use the path with load_data
                df = load_data(temp_file_path)
                st.write("Data loaded successfully!")

            with st.spinner('Calculating features...'):
                feat = compute_features(df)
                st.write("Features computed successfully!")

            with st.spinner('Calculating scores...'):
                scores = score(feat)
                st.write("Scores calculated successfully!")

            st.subheader("Credit Scores")
            st.dataframe(scores.to_frame().rename(columns={0: 'score'}).sort_values(by='score', ascending=False))

            st.subheader("Score Distribution")
            st.bar_chart(scores)

            # Allow downloading the scores as a CSV
            @st.cache_data
            def convert_df_to_csv(df_to_convert):
                return df_to_convert.to_csv().encode('utf-8')

            csv = convert_df_to_csv(scores.to_frame(name='score'))

            st.download_button(
                label="Download scores as CSV",
                data=csv,
                file_name='scores.csv',
                mime='text/csv',
            )
        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)