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
df.columns = df.columns.str.strip().str.replace(' ', '').str.replace('/', '')

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
    fig1 = px.pie(gender_dist, names='Gender', values='count', title="Gender Distribution")
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
    col1.metric("Count of Accounts", f"{df['Customer_ID'].nunique()/1000:.1f}K")
    col2.metric("Total Loan Amount", f"{df['Loan_Amount'].sum()/1e6:.3f}M")
    col3.metric("Total Account Balance", f"{df['Account_Balance'].sum()/1e6:.2f}M")
    col4.metric("Average Interest Rate", f"{df['Interest_Rate'].mean():.2f}")


    # Line chart - Loans by Year
    
    df['Approval_Rejection_Date'] = pd.to_datetime(df['Approval_Rejection_Date'], errors='coerce')

    # Filter valid rows
    filtered_df = df[df['Approval_Rejection_Date'].notna()]
    filtered_df = filtered_df[filtered_df['Loan_ID'].notna()]  # Ensure Loan_ID exists
    filtered_df = filtered_df.drop_duplicates(subset='Loan_ID')  # Remove duplicates
    
    # Extract year
    filtered_df['Loan_Year'] = filtered_df['Approval_Rejection_Date'].dt.year
    
    # Count loans per year
    loan_year_count = filtered_df.groupby('Loan_Year')['Loan_ID'].count().reset_index()
    
    # Plot
    fig = px.line(loan_year_count,x='Loan_Year',y='Loan_ID',text='Loan_ID',markers=True,title="Timely Count of Loans")
    
    fig.update_traces(textposition='top center',texttemplate='%{text:.0f}',marker=dict(size=8))
    fig.update_layout(yaxis_title='Number of Loans',xaxis_title='Year',xaxis=dict(dtick=1))
    
    st.plotly_chart(fig, use_container_width=True)

    # Bar chart - Loan Terms
    loan_term_count = df['Loan_Term'].value_counts().sort_index().reset_index()
    loan_term_count.columns = ['Loan_Term', 'Count']
    
    fig5 = px.bar(loan_term_count, x='Loan_Term', y='Count',text='Count',title="Loan Term wise Loans Count")
    
    fig5.update_traces(textposition='outside',texttemplate='%{text:.0f}')
    fig5.update_layout(yaxis_title='Number of Loans',xaxis_title='Loan Term (months)')
    
    st.plotly_chart(fig5, use_container_width=True)
# 3. Transaction & Financial Analysis
elif section == "Transaction & Financial Analysis":
    st.title("💸 Transaction & Financial Analysis")

    # KPI Cards
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transaction Amount", f"{df['Transaction_Amount'].sum()/1e6:.2f}M")
    col2.metric("Avg Transaction Amount", f"{df['Transaction_Amount'].mean():.2f}")
    col3.metric("No of Transactions", f"{df['TransactionID'].nunique():,}")

    # Extract Month from Transaction_Date
    df['Month'] = pd.to_datetime(df['Transaction_Date'], errors='coerce').dt.strftime('%B')

    # Define calendar month order
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']

    # Group transactions by month
    txn_month = df.groupby('Month')['TransactionID'].nunique().reset_index()
    txn_month.columns = ['Month', 'Count']
    txn_month['Month'] = pd.Categorical(txn_month['Month'], categories=month_order, ordered=True)
    txn_month = txn_month.sort_values('Month')

    # 📈 Line Chart: Monthly Transaction Trends
    fig6 = px.line(txn_month,x='Month',y='Count',text='Count',markers=True,title="Timely Trend of Transactions")

    fig6.update_traces(textposition='top center',texttemplate='%{text:,}',marker=dict(size=8))

    fig6.update_layout(xaxis_title='Month',yaxis_title='Number of Transactions',height=500)

    st.plotly_chart(fig6, use_container_width=True)

    # 📊 Bar Chart: Transaction Type Count
    txn_type_count = df['Transaction_Type'].value_counts().reset_index()
    txn_type_count.columns = ['Transaction_Type', 'Count']

    fig7 = px.bar(txn_type_count,x='Transaction_Type',y='Count',text='Count',title="Transaction Type Count")

    fig7.update_traces(textposition='outside',texttemplate='%{text:,}',textfont_size=12)

    fig7.update_layout(xaxis_title='Transaction Type',yaxis_title='Count',height=500)

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
    # Convert to datetime safely
    df['Last_Credit_Card_Payment_Date'] = pd.to_datetime(df['Last_Credit_Card_Payment_Date'], errors='coerce')
    
    # Extract proper month name
    df['Payment_Month'] = df['Last_Credit_Card_Payment_Date'].dt.strftime('%B')
    
    # Remove rows where month is missing (due to invalid dates)
    df_valid = df.dropna(subset=['Payment_Month', 'Minimum_Payment_Due'])
    
    # Aggregate monthly totals
    monthly_min_due = df_valid.groupby('Payment_Month', observed=False)['Minimum_Payment_Due'].sum().reset_index()
    
    # Ensure calendar order
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    monthly_min_due['Payment_Month'] = pd.Categorical(monthly_min_due['Payment_Month'], categories=month_order, ordered=True)
    monthly_min_due = monthly_min_due.sort_values('Payment_Month')
    
    # Create the bar chart
    fig = px.bar(
        monthly_min_due,
        x='Payment_Month',
        y='Minimum_Payment_Due',
        title="Monthly Minimum Payment Due",
        text='Minimum_Payment_Due'
    )
    
    # Format data labels and layout
    fig.update_traces(
        texttemplate='%{text:,.2f}',  # Comma separator, 2 decimals
        textposition='outside',
        textfont_size=12,
        marker_color='lightskyblue'
    )
    
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Total Minimum Payment Due',
        title_font_size=20,
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_tickfont_size=13,
        yaxis_tickfont_size=13
    )
    
    # Render chart
    st.plotly_chart(fig, use_container_width=True)

    # Combo Chart: Monthly Credit Card Balance vs Limit
    st.subheader("📊 Monthly Trend: Credit Card Balance vs Limit")
    
    # Step 1: Convert Last Credit Card Payment Date to Month
    df['Payment_Month'] = pd.to_datetime(df['Last_Credit_Card_Payment_Date'], errors='coerce').dt.strftime('%B')
    
    # Step 2: Set calendar month order
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    
    # Step 3: Group by month
    monthly_balance = df.groupby('Payment_Month').agg({'Credit_Card_Balance': 'sum','Credit_Limit': 'sum'}).reset_index()
    
    # Step 4: Sort months properly
    monthly_balance['Payment_Month'] = pd.Categorical(monthly_balance['Payment_Month'],categories=month_order,ordered=True)
    monthly_balance = monthly_balance.sort_values('Payment_Month')
    
    # Step 5: Bar chart for Credit Card Balance
    fig9 = px.bar(monthly_balance,x='Payment_Month',y='Credit_Card_Balance',text='Credit_Card_Balance',title="Monthly Credit Card Balance vs Credit Limit")
    
    fig9.update_traces(texttemplate='%{text:,.0f}',textposition='outside',textfont_size=12,name='Credit Card Balance')
    
    # Step 6: Add Credit Limit line chart
    fig9.add_scatter(x=monthly_balance['Payment_Month'],y=monthly_balance['Credit_Limit'],mode='lines+markers+text',name='Credit Limit',
        text=monthly_balance['Credit_Limit'],textposition='top center',texttemplate='%{text:,.0f}')
    
    # Step 7: Layout styling
    fig9.update_layout(xaxis_title='Month',yaxis_title='Amount (₹)',title_font_size=20,legend_title_text='Metric',height=550)
    
    # Step 8: Show chart
    st.plotly_chart(fig9, use_container_width=True)
