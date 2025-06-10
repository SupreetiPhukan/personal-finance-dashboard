import streamlit as st
import pandas as pd
import plotly.express as px

# Page config and title
st.set_page_config(page_title="Personal Finance Tracker", layout="wide")
st.title("📊 Personal Financial Dashboard")

# Sidebar Inputs
st.sidebar.header("Enter Monthly Financial Data")
month = st.sidebar.selectbox(
    "Select Month", [
        "January", "February", "March", "April", "May", "June", 
        "July", "August", "September", "October", "November", "December"
    ]
)
income = st.sidebar.number_input("Monthly Income (₹)", min_value=0, step=500)

# AI-based Smart Budget Recommendations
st.sidebar.markdown("### 🤖 Smart Budget Recommendations")
if income > 0:
    ai_budget = {
        "Rent": income * 0.30,
        "Groceries": income * 0.20,
        "Transport": income * 0.10,
        "Utilities": income * 0.10,
        "Entertainment": income * 0.10,
        "Others": income * 0.10,
        "Savings": income * 0.10
    }
    for category, value in ai_budget.items():
        st.sidebar.write(f"{category}: ₹{int(value)}")
else:
    st.sidebar.info("Enter income to get AI-based recommendations.")

# Expense Inputs
expenses = {
    "Rent": st.sidebar.number_input("Rent (₹)", min_value=0, step=100),
    "Groceries": st.sidebar.number_input("Groceries (₹)", min_value=0, step=100),
    "Transport": st.sidebar.number_input("Transport (₹)", min_value=0, step=100),
    "Utilities": st.sidebar.number_input("Utilities (₹)", min_value=0, step=100),
    "Entertainment": st.sidebar.number_input("Entertainment (₹)", min_value=0, step=100),
    "Others": st.sidebar.number_input("Others (₹)", min_value=0, step=100)
}

goal = st.sidebar.number_input("Savings Goal (₹)", min_value=0, step=1000)

# Financial Calculations
total_expense = sum(expenses.values())
savings = income - total_expense
saving_percent = (savings / income * 100) if income > 0 else 0

# Summary Display
st.subheader(f"📅 Financial Summary for {month}")
col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"₹{income}")
col2.metric("Total Expenses", f"₹{total_expense}")
col3.metric("Total Savings", f"₹{savings}")

# Pie Chart for Expense Distribution
expense_df = pd.DataFrame({
    "Category": expenses.keys(),
    "Amount": expenses.values()
})
if total_expense > 0:
    pie_chart = px.pie(expense_df, values="Amount", names="Category", title="Expense Distribution")
    st.plotly_chart(pie_chart, use_container_width=True)

# Savings Goal Progress
if goal > 0:
    st.subheader("🎯 Savings Goal Progress")
    safe_savings = max(0, savings)
    progress = min(safe_savings / goal, 1.0)
    st.progress(progress)
    st.write(f"Saved ₹{savings} of ₹{goal} ({int(progress * 100)}%)")
else:
    st.info("Set a savings goal in the sidebar to track progress.")

# 📈 Predicted Savings Next Month
if income > 0:
    predicted_savings = savings * 1.05
    st.subheader("📈 AI Forecast")
    st.success(f"Predicted Savings Next Month: ₹{int(predicted_savings)} (Estimated +5%)")

# 🧠 Simple AI Chat Assistant
st.sidebar.markdown("---")
st.sidebar.markdown("### 💬 Ask Finance Assistant")
user_query = st.sidebar.text_input("Type a question")

if user_query:
    q = user_query.lower()
    if "rent" in q:
        st.sidebar.success(f"You spent ₹{expenses['Rent']} on Rent.")
    elif "savings goal" in q or "goal" in q:
        if savings >= goal:
            st.sidebar.success("🎉 You’ve achieved your savings goal!")
        else:
            st.sidebar.info(f"You're ₹{goal - savings} away from your goal.")
    elif "savings" in q:
        st.sidebar.info(f"Your current savings: ₹{savings}")
    elif "expenses" in q:
        st.sidebar.info(f"Your total expenses: ₹{total_expense}")
    else:
        st.sidebar.warning("I’m still learning! Try asking about 'rent', 'savings', or 'goal'.")

# Optional Table View
if st.checkbox("Show Expense Table"):
    st.dataframe(expense_df.set_index("Category"))

# Footer
st.markdown("---")
st.markdown("🔐 Your data stays in your browser. Nothing is stored or uploaded.")
