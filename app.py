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
file_path = "Comprehensive_Banking_Database_ main.csv"  # Ensure this CSV is available in your environment
df = pd.read_csv(file_path)
df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('/', '_')

# Sidebar Navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Choose a Section", (
    "Customer Demographics & Overview",
    "Accounts & Loan Analysis",
    "Transaction & Financial Analysis",
    "Credit Card Analysis"
))

# 1. Customer Demographics & Overview
if section == "Customer Demographics & Overview":
    st.title("📊 Customer Demographics & Overview")

    # KPI Cards
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Count of Customers", f"{df['Customer_ID'].nunique()/1000:.1f}K")
    col2.metric("Avg of Customers Age", f"{df['Age'].mean():.2f}")
    col3.metric("Male Customers Count", f"{(df['Gender']=='Male').sum()/1000:.2f}K")
    col4.metric("Female Customers Count", f"{(df['Gender']=='Female').sum()/1000:.2f}K")
    col5.metric("Other Customers Count", f"{(df['Gender']=='Other').sum()/1000:.2f}K")

    # Pie chart - Gender
    gender_dist = df['Gender'].value_counts().reset_index()
    gender_dist.columns = ['Gender', 'count']  # Rename correctly
    fig1 = px.pie(
    gender_dist, 
    names='Gender', 
    values='count', 
    title="Gender Distribution",
    hole=0.4)
    fig1.update_traces(textposition='inside', textinfo='label+percent+value')
    st.plotly_chart(fig1, use_container_width=True)

    # Age Group
    bins = [0, 30, 40, 50, 60, 70]
    labels = ['18-30', '31-40', '41-50', '51-60', '61-70']
    df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
    age_group_counts = df['Age_Group'].value_counts().sort_index()
    fig2 = px.bar(
    x=age_group_counts.index, 
    y=age_group_counts.values,
    labels={'x': 'Age Group', 'y': 'Count of Customers'},
    title="Age Group wise Number of Customers",
    text=age_group_counts.values)
    fig2.update_traces(textposition='outside', textfont_size=12)
    st.plotly_chart(fig2, use_container_width=True)

    # City-wise bar chart
    city_count = df['City'].value_counts().reset_index()
    city_count.columns = ['City', 'Count']
    fig3 = px.bar(
    city_count, 
    x='Count', 
    y='City', 
    orientation='h', 
    title="Count of Customers by City",
    text='Count',
    height=900 )
    fig3.update_traces(textposition='outside', textfont_size=12)
    st.plotly_chart(fig3, use_container_width=True)

# 2. Accounts & Loan Analysis
elif section == "Accounts & Loan Analysis":
    st.title("💳 Accounts & Loan Analysis")

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Count of Accounts", f"{df['Account_ID'].nunique()/1000:.1f}K")
    col2.metric("Total Loan Amount", f"{df['Loan_Amount'].sum()/1e6:.3f}M")
    col3.metric("Total Account Balance", f"{df['Account_Balance'].sum()/1e6:.2f}M")
    col4.metric("Average Interest Rate", f"{df['Interest_Rate'].mean():.2f}")

    # Line chart - Loans by Year
    df['Loan_Year'] = pd.to_datetime(df['Approval_Rejection_Date'], errors='coerce').dt.year
    loan_year_count = df.groupby('Loan_Year')['Loan_ID'].count().reset_index()
    fig4 = px.line(loan_year_count, x='Loan_Year', y='Loan_ID', markers=True, title="Timely Count of Loans")
    st.plotly_chart(fig4, use_container_width=True)

    # Bar chart - Loan Terms
    loan_term_count = df['Loan_Term'].value_counts().sort_index().reset_index()
    loan_term_count.columns = ['Loan_Term', 'Count']
    fig5 = px.bar(loan_term_count, x='Loan_Term', y='Count', title="Loan Term wise Loans Count")
    st.plotly_chart(fig5, use_container_width=True)

# 3. Transaction & Financial Analysis
elif section == "Transaction & Financial Analysis":
    st.title("💸 Transaction & Financial Analysis")

    # KPI Cards
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transaction Amount", f"{df['Transaction_Amount'].sum()/1e6:.2f}M")
    col2.metric("Avg Transaction Amount", f"{df['Transaction_Amount'].mean():.2f}")
    col3.metric("No of Transactions", f"{df['TransactionID'].nunique():,}")

    # Monthly Trends
    df['Month'] = pd.to_datetime(df['Transaction_Date'], errors='coerce').dt.month_name()
    df['Month'] = pd.Categorical(df['Month'], categories=[
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ], ordered=True)

    txn_month = df['Month'].value_counts().sort_index().reset_index()
    txn_month.columns = ['Month', 'Count']

    fig6 = px.line(txn_month, x='Month', y='Count', text='Count_of_Transactions', markers=True,
                   title="Timely Trend of Transactions")
    fig6.update_traces(textposition="top center", textfont_size=12)
    st.plotly_chart(fig6, use_container_width=True)

    # Transaction Type
    txn_type_count = df['Transaction_Type'].value_counts().reset_index()
    txn_type_count.columns = ['Transaction_Type', 'Count']

    fig7 = px.bar(txn_type_count, x='Transaction_Type', y='No_of_Loans', text='Count',
                  title="Transaction Type Count")
    fig7.update_traces(textposition='outside', textfont_size=12)
    st.plotly_chart(fig7, use_container_width=True)

# 4. Credit Card Analysis
elif section == "Credit Card Analysis":
    st.title("💳 Credit Card Analysis")

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Count of CardID", f"{df['CardID'].nunique()}")
    col2.metric("Total Credit Card Balance", f"{df['Credit_Card_Balance'].sum()/1e6:.2f}M")
    col3.metric("Total Minimum Payment Due", f"{df['Minimum_Payment_Due'].sum()/1e3:.2f}K")
    col4.metric("Total Rewards Points", f"{df['Rewards_Points'].sum()/1e6:.2f}M")

    # Bar Chart - Monthly Payments
    df['Payment_Month'] = pd.to_datetime(df['Last_Credit_Card_Payment_Date'], errors='coerce').dt.month_name()
    min_payment = df.groupby('Payment_Month')['Minimum_Payment_Due'].sum().reset_index()
    fig8 = px.bar(min_payment, x='Payment_Month', y='Minimum_Payment_Due', title="Monthly Minimum Payment Due")
    st.plotly_chart(fig8, use_container_width=True)

    # Combo Chart
    monthly_balance = df.groupby('Payment_Month').agg({
        'Credit_Card_Balance': 'sum',
        'Credit_Limit': 'sum'
    }).reset_index()
    fig9 = px.bar(monthly_balance, x='Payment_Month', y='Credit_Card_Balance', title="Credit Card Balance vs Limit")
    fig9.add_scatter(x=monthly_balance['Payment_Month'], y=monthly_balance['Credit_Limit'], mode='lines+markers', name='Credit Limit')
    st.plotly_chart(fig9, use_container_width=True)
