# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Set Streamlit page config
st.set_page_config(page_title="Banking Risk Dashboard", layout="wide")

# Simple login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login to Banking Dashboard")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "Banking_Analytics" and password == "Secure123":
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials.")
    st.stop()

# Load dataset
file_path = "Comprehensive_Banking_Database_ main.csv"
df = pd.read_csv(file_path)
df.columns = df.columns.str.strip().str.replace(' ', '').str.replace('/', '')

# Convert datetime columns
if 'Approval_Rejection_Date' in df.columns:
    df['Approval_Rejection_Date'] = pd.to_datetime(df['Approval_Rejection_Date'], errors='coerce')
if 'Transaction_Date' in df.columns:
    df['Transaction_Date'] = pd.to_datetime(df['Transaction_Date'], errors='coerce')
if 'Last_Credit_Card_Payment_Date' in df.columns:
    df['Last_Credit_Card_Payment_Date'] = pd.to_datetime(df['Last_Credit_Card_Payment_Date'], errors='coerce')

# Add Month and Quarter columns for filtering
if 'Transaction_Date' in df.columns:
    df['Month'] = df['Transaction_Date'].dt.strftime('%B')
    df['Quarter'] = df['Transaction_Date'].dt.to_period('Q').astype(str)

# Sidebar Navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Choose a Section", (
    "Customer Demographics & Overview",
    "Accounts & Loan Analysis",
    "Transaction & Financial Analysis",
    "Credit Card Analysis"
))

# Sidebar filters
st.sidebar.header("🔍 Filters")
selected_gender = st.sidebar.multiselect("Gender", df['Gender'].dropna().unique(), default=df['Gender'].dropna().unique())
selected_months = st.sidebar.multiselect("Month", df['Month'].dropna().unique(), default=df['Month'].dropna().unique())
selected_quarters = st.sidebar.multiselect("Quarter", df['Quarter'].dropna().unique(), default=df['Quarter'].dropna().unique())
selected_card_type = st.sidebar.multiselect("Card Type", df['Card_Type'].dropna().unique(), default=df['Card_Type'].dropna().unique())
selected_account_type = st.sidebar.multiselect("Account Type", df['Account_Type'].dropna().unique(), default=df['Account_Type'].dropna().unique())

# Apply filters
filtered_df = df[
    df['Gender'].isin(selected_gender) &
    df['Month'].isin(selected_months) &
    df['Quarter'].isin(selected_quarters) &
    df['Card_Type'].isin(selected_card_type) &
    df['Account_Type'].isin(selected_account_type)
]

# Now use filtered_df in place of df throughout your visualizations

# Example section: Customer Demographics & Overview
if section == "Customer Demographics & Overview":
    st.title("📊 Customer Demographics & Overview")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Count of Customers", f"{filtered_df['Customer_ID'].nunique()/1000:.1f}K")
    col2.metric("Avg of Customers Age", f"{filtered_df['Age'].mean():.2f}")
    col3.metric("Male Customers Count", f"{(filtered_df['Gender']=='Male').sum()/1000:.2f}K")
    col4.metric("Female Customers Count", f"{(filtered_df['Gender']=='Female').sum()/1000:.2f}K")
    col5.metric("Other Customers Count", f"{(filtered_df['Gender']=='Other').sum()/1000:.2f}K")

    gender_dist = filtered_df['Gender'].value_counts().reset_index()
    gender_dist.columns = ['Gender', 'count']
    fig1 = px.pie(gender_dist, names='Gender', values='count', title="Gender Distribution")
    st.plotly_chart(fig1, use_container_width=True)

    bins = [0, 30, 40, 50, 60, 70]
    labels = ['18-30', '31-40', '41-50', '51-60', '61-70']
    filtered_df['Age_Group'] = pd.cut(filtered_df['Age'], bins=bins, labels=labels, right=False)
    age_group_counts = filtered_df['Age_Group'].value_counts().sort_index()
    fig2 = px.bar(
        x=age_group_counts.index,
        y=age_group_counts.values,
        labels={'x': 'Age Group', 'y': 'Count of Customers'},
        title="Age Group wise Number of Customers",
        text=age_group_counts.values
    )
    fig2.update_traces(textposition='outside', textfont_size=12)
    st.plotly_chart(fig2, use_container_width=True)

    city_count = filtered_df['City'].value_counts().reset_index()
    city_count.columns = ['City', 'Count']
    fig3 = px.bar(city_count, x='Count', y='City', orientation='h', title="Count of Customers by City", text='Count', height=900)
    fig3.update_traces(textposition='outside', textfont_size=12)
    st.plotly_chart(fig3, use_container_width=True)
