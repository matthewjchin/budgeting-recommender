import streamlit as st
import pandas as pd
import plotly.express as px

# from google.cloud import firestore

# When running this file, the following command should be used:
# `streamlit run interface_test.py`

# # Create instance of database storing all info added
# db = firestore.Client()

st.title("Budget Tracker")

# Add transaction
with st.form("add_transaction"):
    description = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.0)
    category = st.selectbox("Category", ["Food", "Transport", "Bills"])
    
    # if st.form_submit_button("Add"):
        # db.collection('transactions').add({
        # #     'description': description,
        # #     'amount': amount,
        #     'category': category,
        #     'date': firestore.SERVER_TIMESTAMP
        # })
        # st.success("Added!")

# Show charts
df = pd.DataFrame([{"description": description, "amount": amount, "category": category}])  # Your transaction data
fig = px.pie(df, values='amount', names='category')
st.plotly_chart(fig)