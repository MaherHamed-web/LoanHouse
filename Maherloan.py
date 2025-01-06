import streamlit as st

# Simple Interest Loan Calculator
def calculate_simple_interest(principal, annual_rate, years):
    total_interest = principal * (annual_rate / 100) * years
    total_loan_cost = principal + total_interest
    monthly_payment = total_loan_cost / (years * 12)
    return total_interest, total_loan_cost, monthly_payment

# Streamlit App
st.title("Simple Interest Loan Calculator")

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
