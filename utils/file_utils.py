import pandas as pd
import streamlit as st

def read_csv(uploaded_file):
    """Reads a CSV file and returns a pandas DataFrame."""
    try:
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")
        return df
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None
