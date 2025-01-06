import streamlit as st
import pandas as pd

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
            "Balance": max(balance, 0)  # Ensure balance doesn't go negative
        })

    return pd.DataFrame(schedule)

# Streamlit App
st.title("Simple Interest Loan Calculator with Amortization Schedule")

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

# Generate and Display Amortization Schedule
if st.checkbox("Show Amortization Schedule"):
    schedule = generate_amortization_schedule(loan_amount, interest_rate, loan_term, monthly_payment)
    st.subheader("Amortization Schedule")
    st.dataframe(schedule)

    # Allow user to download the schedule
    csv = schedule.to_csv(index=False)
    st.download_button("Download Amortization Schedule as CSV", data=csv, file_name="amortization_schedule.csv", mime="text/csv")
