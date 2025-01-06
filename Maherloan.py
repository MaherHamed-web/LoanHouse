import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Simple Interest Loan Calculator
def calculate_simple_interest(principal, annual_rate, years):
    total_interest = principal * (annual_rate / 100) * years
    total_loan_cost = principal + total_interest
    monthly_payment = total_loan_cost / (years * 12)
    return total_interest, total_loan_cost, monthly_payment

# Generate Amortization Schedule
def generate_amortization_schedule(principal, annual_rate, years, monthly_payment):
    total_months = years * 12
    monthly_interest = (principal * (annual_rate / 100)) / total_months
    balance = principal
    schedule = []

    for month in range(1, total_months + 1):
        interest_payment = monthly_interest
        principal_payment = monthly_payment - interest_payment
        balance -= principal_payment
        schedule.append({
            "Month": month,
            "Payment": monthly_payment,
            "Principal": principal_payment,
            "Interest": interest_payment,
            "Balance": max(balance, 0)
        })

    return pd.DataFrame(schedule)

# Streamlit App
st.title("Simple Interest Loan Calculator with Graphs")

# User Inputs
loan_amount = st.number_input("Loan Amount ($)", value=100000, step=1000)
interest_rate = st.number_input("Interest Rate (Annual %)", value=1.0, step=0.1)
loan_term = st.slider("Loan Term (Years)", 1, 30, 5)

# Calculate Loan Details
total_interest, total_loan_cost, monthly_payment = calculate_simple_interest(loan_amount, interest_rate, loan_term)

# Display Results
st.subheader("Loan Details")
st.write(f"Principal: ${loan_amount:,.2f}")
st.write(f"Total Interest: ${total_interest:,.2f}")
st.write(f"Total Loan Cost: ${total_loan_cost:,.2f}")
st.write(f"Monthly Payment: ${monthly_payment:,.2f}")

# Generate Amortization Schedule
schedule = generate_amortization_schedule(loan_amount, interest_rate, loan_term, monthly_payment)

# Show Graphs
st.subheader("Graphs")

# 1. Payment Breakdown Over Time
if st.checkbox("Show Payment Breakdown Over Time"):
    plt.figure(figsize=(10, 5))
    plt.plot(schedule["Month"], schedule["Principal"], label="Principal Payment")
    plt.plot(schedule["Month"], schedule["Interest"], label="Interest Payment")
    plt.title("Payment Breakdown Over Time")
    plt.xlabel("Month")
    plt.ylabel("Amount ($)")
    plt.legend()
    st.pyplot(plt)

# 2. Balance Over Time
if st.checkbox("Show Balance Over Time"):
    plt.figure(figsize=(10, 5))
    plt.plot(schedule["Month"], schedule["Balance"], label="Remaining Balance", color="green")
    plt.title("Balance Over Time")
    plt.xlabel("Month")
    plt.ylabel("Remaining Balance ($)")
    plt.legend()
    st.pyplot(plt)

# 3. Cumulative Payments
if st.checkbox("Show Cumulative Payments"):
    schedule["Cumulative Principal"] = schedule["Principal"].cumsum()
    schedule["Cumulative Interest"] = schedule["Interest"].cumsum()
    plt.figure(figsize=(10, 5))
    plt.plot(schedule["Month"], schedule["Cumulative Principal"], label="Cumulative Principal")
    plt.plot(schedule["Month"], schedule["Cumulative Interest"], label="Cumulative Interest")
    plt.title("Cumulative Payments Over Time")
    plt.xlabel("Month")
    plt.ylabel("Amount ($)")
    plt.legend()
    st.pyplot(plt)

# 4. Loan Summary Pie Chart
if st.checkbox("Show Loan Summary Pie Chart"):
    labels = ["Principal", "Total Interest"]
    sizes = [loan_amount, total_interest]
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=["#1f77b4", "#ff7f0e"])
    plt.title("Loan Summary: Principal vs Interest")
    st.pyplot(plt)

# Allow user to download the schedule
if st.checkbox("Show Amortization Schedule"):
    st.subheader("Amortization Schedule")
    st.dataframe(schedule)

    csv = schedule.to_csv(index=False)
    st.download_button("Download Amortization Schedule as CSV", data=csv, file_name="amortization_schedule.csv", mime="text/csv")
