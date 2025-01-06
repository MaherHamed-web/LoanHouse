import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Loan Calculator Function
def calculate_monthly_payment(principal, annual_rate, years):
    monthly_rate = annual_rate / 12 / 100
    n_payments = years * 12
    monthly_payment = principal * (monthly_rate * (1 + monthly_rate)**n_payments) / ((1 + monthly_rate)**n_payments - 1)
    return monthly_payment

# Streamlit App
st.title("Home Loan Calculator")

# User Inputs
loan_amount = st.number_input("Loan Amount ($)", value=250000, step=1000)
interest_rate = st.number_input("Interest Rate (Annual %)", value=3.5, step=0.1)
loan_term = st.slider("Loan Term (Years)", 1, 30, 15)
down_payment = st.number_input("Down Payment ($)", value=0, step=1000)

# Calculate Loan Details
principal = loan_amount - down_payment
monthly_payment = calculate_monthly_payment(principal, interest_rate, loan_term)

# Display Results
st.subheader("Loan Details")
st.write(f"Principal: ${principal:,.2f}")
st.write(f"Monthly Payment: ${monthly_payment:,.2f}")

# Amortization Schedule
if st.checkbox("Show Amortization Schedule"):
    monthly_rate = interest_rate / 12 / 100
    n_payments = loan_term * 12
    balance = principal
    schedule = []
    
    for i in range(1, n_payments + 1):
        interest = balance * monthly_rate
        principal_payment = monthly_payment - interest
        balance -= principal_payment
        schedule.append([i, monthly_payment, principal_payment, interest, balance])
    
    df = pd.DataFrame(schedule, columns=["Month", "Payment", "Principal", "Interest", "Balance"])
    st.dataframe(df)

    # Plot the Payment Breakdown
    fig, ax = plt.subplots()
    ax.plot(df["Month"], df["Principal"], label="Principal Paid")
    ax.plot(df["Month"], df["Interest"], label="Interest Paid")
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount ($)")
    ax.set_title("Payment Breakdown Over Time")
    ax.legend()
    st.pyplot(fig)
