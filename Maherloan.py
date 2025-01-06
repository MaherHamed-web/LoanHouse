import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Translation Dictionary
translations = {
    "ar": {
        "title": "حاسبة القرض البسيط",
        "dedication": "تم التطوير بواسطة ماهر العروي، إلى فيصل، أخيه الحبيب.",
        "calculation_mode": "اختر وضع الحساب:",
        "calculate_monthly_payment": "حساب القسط الشهري",
        "calculate_loan_amount": "حساب مبلغ القرض",
        "loan_amount": "مبلغ القرض ($)",
        "down_payment": "الدفعة المقدمة ($)",
        "interest_rate": "نسبة الفائدة السنوية (%)",
        "loan_term": "مدة القرض (بالسنوات)",
        "monthly_payment": "القسط الشهري ($)",
        "desired_monthly_payment": "القسط الشهري المطلوب ($)",
        "principal": "المبلغ الأساسي",
        "total_interest": "إجمالي الفائدة",
        "total_loan_cost": "التكلفة الإجمالية للقرض",
        "loan_summary": "ملخص القرض: المبلغ الأساسي مقابل الفائدة",
        "amortization_schedule": "جدول السداد",
        "download_csv": "تحميل جدول السداد كملف CSV"
    },
    "en": {
        "title": "Simple Interest Loan Calculator",
        "dedication": "Developed by Maher Alerwi, to Faisal, his beloved brother.",
        "calculation_mode": "Choose Calculation Mode:",
        "calculate_monthly_payment": "Calculate Monthly Payment",
        "calculate_loan_amount": "Calculate Loan Amount",
        "loan_amount": "Loan Amount ($)",
        "down_payment": "Down Payment ($)",
        "interest_rate": "Interest Rate (Annual %)",
        "loan_term": "Loan Term (Years)",
        "monthly_payment": "Monthly Payment ($)",
        "desired_monthly_payment": "Desired Monthly Payment ($)",
        "principal": "Principal",
        "total_interest": "Total Interest",
        "total_loan_cost": "Total Loan Cost",
        "loan_summary": "Loan Summary: Principal vs Interest",
        "amortization_schedule": "Amortization Schedule",
        "download_csv": "Download Amortization Schedule as CSV"
    }
}

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
# Language Toggle
language = st.radio("Select Language / اختر اللغة:", ["العربية", "English"], index=0)
lang = "ar" if language == "العربية" else "en"

# Titles and Dedication
st.title(translations[lang]["title"])
st.write(f"**{translations[lang]['dedication']}**")

# Toggle to select calculation mode
calculation_mode = st.radio(translations[lang]["calculation_mode"], [
    translations[lang]["calculate_monthly_payment"],
    translations[lang]["calculate_loan_amount"]
])

if calculation_mode == translations[lang]["calculate_monthly_payment"]:
    # User Inputs for Monthly Payment Calculation
    st.subheader(translations[lang]["calculate_monthly_payment"])
    loan_amount = st.number_input(translations[lang]["loan_amount"], value=100000, step=1000)
    down_payment = st.number_input(translations[lang]["down_payment"], value=0, step=1000)
    interest_rate = st.number_input(translations[lang]["interest_rate"], value=1.0, step=0.1)
    loan_term = st.slider(translations[lang]["loan_term"], 1, 30, 5)

    # Adjust principal based on down payment
    principal = loan_amount - down_payment

    # Calculate Loan Details
    total_interest, total_loan_cost, monthly_payment = calculate_simple_interest(principal, interest_rate, loan_term)

    # Display Results
    st.write(f"{translations[lang]['principal']}: ${principal:,.2f}")
    st.write(f"{translations[lang]['total_interest']}: ${total_interest:,.2f}")
    st.write(f"{translations[lang]['total_loan_cost']}: ${total_loan_cost:,.2f}")
    st.write(f"{translations[lang]['monthly_payment']}: ${monthly_payment:,.2f}")

    # Loan Summary Pie Chart
    st.subheader(translations[lang]["loan_summary"])
    labels = [translations[lang]["principal"], translations[lang]["total_interest"]]
    sizes = [principal, total_interest]
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=["#1f77b4", "#ff7f0e"])
    plt.title(translations[lang]["loan_summary"])
    st.pyplot(plt)

    # Amortization Schedule
    st.subheader(translations[lang]["amortization_schedule"])
    schedule = generate_amortization_schedule(principal, interest_rate, loan_term, monthly_payment)
    st.dataframe(schedule)

    # Allow user to download the schedule
    csv = schedule.to_csv(index=False)
    st.download_button(translations[lang]["download_csv"], data=csv, file_name="amortization_schedule.csv", mime="text/csv")

else:
    # User Inputs for Loan Amount Calculation
    st.subheader(translations[lang]["calculate_loan_amount"])
    monthly_payment = st.number_input(translations[lang]["desired_monthly_payment"], value=1500, step=100)
    interest_rate = st.number_input(translations[lang]["interest_rate"], value=1.0, step=0.1)
    loan_term = st.slider(translations[lang]["loan_term"], 1, 30, 5)

    # Calculate Loan Details
    principal, total_interest, total_loan_cost = calculate_loan_amount(monthly_payment, interest_rate, loan_term)

    # Display Results
    st.write(f"{translations[lang]['desired_monthly_payment']}: ${monthly_payment:,.2f}")
    st.write(f"{translations[lang]['principal']}: ${principal:,.2f}")
    st.write(f"{translations[lang]['total_interest']}: ${total_interest:,.2f}")
    st.write(f"{translations[lang]['total_loan_cost']}: ${total_loan_cost:,.2f}")

    # Loan Summary Pie Chart
    st.subheader(translations[lang]["loan_summary"])
    labels = [translations[lang]["principal"], translations[lang]["total_interest"]]
    sizes = [principal, total_interest]
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=["#1f77b4", "#ff7f0e"])
    plt.title(translations[lang]["loan_summary"])
    st.pyplot(plt)
