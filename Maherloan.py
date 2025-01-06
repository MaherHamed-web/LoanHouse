import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to calculate loan details for given principal
def calculate_simple_interest(principal, annual_rate, years):
    total_interest = principal * (annual_rate / 100) * years
    total_loan_cost = principal + total_interest
    monthly_payment = total_loan_cost / (years * 12)
    return total_interest, total_loan_cost, monthly_payment

# Function to calculate principal based on monthly payment
def calculate_loan_amount(monthly_payment, annual_rate, years):
    total_months = years * 12
    total_interest_rate = (annual_rate / 100) * years
    principal = monthly_payment * total_months / (1 + total_interest_rate)
    total_interest = principal * total_interest_rate
    total_loan_cost = principal + total_interest
    return principal, total_interest, total_loan_cost

# Function to generate amortization schedule
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
st.title("Simple Interest Loan Calculator")

# Toggle to select calculation mode
calculation_mode = st.radio("Choose Calculation Mode:", ["Calculate Monthly Payment", "Calculate Loan Amount"])

if calculation_mode == "Calculate Monthly Payment":
    # User Inputs for Monthly Payment Calculation
    st.subheader("Calculate Monthly Payment")
    loan_amount = st.number_input("Loan Amount ($)", value=100000, step=1000)
    interest_rate = st.number_input("Interest Rate (Annual %)", value=1.0, step=0.1)
    loan_term = st.slider("Loan Term (Years)", 1, 30, 5)

    # Calculate Loan Details
    total_interest, total_loan_cost, monthly_payment = calculate_simple_interest(loan_amount, interest_rate, loan_term)

    # Display Results
    st.write(f"Principal: ${loan_amount:,.2f}")
    st.write(f"Total Interest: ${total_interest:,.2f}")
    st.write(f"Total Loan Cost: ${total_loan_cost:,.2f}")
    st.write(f"Monthly Payment: ${monthly_payment:,.2f}")

    # Loan Summary Pie Chart
    st.subheader("Loan Summary: Principal vs Interest")
    labels = ["Principal", "Total Interest"]
    sizes = [loan_amount, total_interest]
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=["#1f77b4", "#ff7f0e"])
    plt.title("Loan Summary: Principal vs Interest")
    st.pyplot(plt)

    # Amortization Schedule
    st.subheader("Amortization Schedule")
    schedule = generate_amortization_schedule(loan_amount, interest_rate, loan_term, monthly_payment)
    st.dataframe(schedule)

    # Allow user to download the schedule
    csv = schedule.to_csv(index=False)
    st.download_button("Download Amortization Schedule as CSV", data=csv, file_name="amortization_schedule.csv", mime="text/csv")

else:
    # User Inputs for Loan Amount Calculation
    st.subheader("Calculate Loan Amount")
    monthly_payment = st.number_input("Desired Monthly Payment ($)", value=1500, step=100)
    interest_rate = st.number_input("Interest Rate (Annual %)", value=1.0, step=0.1)
    loan_term = st.slider("Loan Term (Years)", 1, 30, 5)

    # Calculate Loan Details
    principal, total_interest, total_loan_cost = calculate_loan_amount(monthly_payment, interest_rate, loan_term)

    # Display Results
    st.write(f"Desired Monthly Payment: ${monthly_payment:,.2f}")
    st.write(f"Loan Amount Bank Can Lend: ${principal:,.2f}")
    st.write(f"Total Interest: ${total_interest:,.2f}")
    st.write(f"Total Loan Cost: ${total_loan_cost:,.2f}")

    # Loan Summary Pie Chart
    st.subheader("Loan Summary: Principal vs Interest")
    labels = ["Principal", "Total Interest"]
    sizes = [principal, total_interest]
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=["#1f77b4", "#ff7f0e"])
    plt.title("Loan Summary: Principal vs Interest")
    st.pyplot(plt)
