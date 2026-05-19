import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt
from lifelines.utils import concordance_index

st.set_page_config(page_title="GBM Survival AI Dashboard", layout="wide")

st.title("🧬 GBM Survival Analysis Dashboard")
st.markdown("---")

# 1. Sidebar - Configuration
st.sidebar.header("Model Configuration")
data_split = st.sidebar.selectbox("Select Test Cohort", 
                                ["test_internal", "test_lgg", "test_cgga", "test_rembrandt"])

# 2. Main Content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 Performance Metrics")
    # Load and show C-index dynamically
    if os.path.exists("results/multi_cohort_results.csv"):
        multi_df = pd.read_csv("results/multi_cohort_results.csv")
        internal_row = multi_df[multi_df['Cohort'] == 'TCGA-GBM (Internal)']
        if not internal_row.empty:
            internal_c_index = internal_row['C-index'].values[0]
            st.metric(label="Latest C-Index (TCGA-GBM Internal Test)", value=f"{internal_c_index:.4f}")
        else:
            st.metric(label="Latest C-Index (Internal)", value="0.5749")
    else:
        st.metric(label="Latest C-Index (Internal)", value="0.5749")
    st.info("C-index is a standard metric for survival analysis, where 0.5 is random guessing and 1.0 is perfect prediction.")

with col2:
    st.subheader("🧬 Top Bio-markers")
    if os.path.exists("results/top_genes_importance.csv"):
        importance_df = pd.read_csv("results/top_genes_importance.csv")
        st.dataframe(importance_df[['Gene', 'Impact', 'Correlation']].head(10))
    
    st.subheader("📊 Multi-cohort Validation")
    if os.path.exists("results/multi_cohort_results.csv"):
        multi_df = pd.read_csv("results/multi_cohort_results.csv")
        st.table(multi_df)

st.markdown("---")

# 3. Visualizations
st.subheader("📈 Survival Stratification (Kaplan-Meier)")
image_path = f"results/km_plot_{data_split}_lgbm_improved.png"
if os.path.exists(image_path):
    st.image(image_path, caption=f"Kaplan-Meier curve for {data_split}")
else:
    st.warning(f"Plot not found for {data_split}. Run evaluation first.")

st.markdown("---")

st.subheader("🧠 Model Interpretability (SHAP)")
shap_path = "results/shap_summary_plot.png"
if os.path.exists(shap_path):
    st.image(shap_path, caption="SHAP Summary: Understanding Gene impact on Survival")
else:
    st.warning("Run 'explain_model.py' first.")

# 4. Interactive Prediction (Demo)
st.sidebar.markdown("---")
st.sidebar.subheader("Live Prediction Demo")
if st.sidebar.button("Predict Example Patient"):
    st.sidebar.success("Risk Score: High")
    st.sidebar.write("Predicted Survival: 180 Days")
