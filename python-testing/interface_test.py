import streamlit as st
import pandas as pd
import plotly.express as px

# When running this file, the following command should be used:
# `streamlit run interface_test.py`


st.title("Budget Tracker")

# Add transaction form
with st.form("add_transaction"):
    description = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.0)
    category = st.selectbox("Category", ["Food", "Transport", "Bills"])
    if st.form_submit_button("Add"):
        # Save transaction
        st.success("Added!")

# Show charts
df = pd.DataFrame([{"description": description, "amount": amount, "category": category}])  # Your transaction data
fig = px.pie(df, values='amount', names='category')
st.plotly_chart(fig)