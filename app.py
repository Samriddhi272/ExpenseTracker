import streamlit as st
import pandas as pd
from datetime import datetime
from expense import Expense   

EXPENSE_FILE = "expenses.csv"

def write_expense_to_file(expense: Expense, file_path=EXPENSE_FILE):
    with open(file_path, 'a') as f:
        f.write(f"{expense.name},{expense.amount},{expense.category},{expense.date}\n")

def read_expenses_from_file(file_path, start_date, end_date):
    expenses = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) != 4:
                    continue
                expense_name, expense_amount, expense_category, expense_date = parts
                try:
                    expense_dt = datetime.strptime(expense_date, "%Y-%m-%d").date()
                except ValueError:
                    continue
                if start_date <= expense_dt <=  end_date:
                    expenses.append(Expense(
                        name=expense_name,
                        amount=float(expense_amount),
                        category=expense_category,
                        date=expense_date
                    ))
    except FileNotFoundError:
        pass
    return expenses

def main():
    st.title("Expense Tracker")

    st.header("Add New Expense")
    with st.form("expense_form", clear_on_submit=True):
        name = st.text_input("Expense Name")
        amount_str = st.text_input("Amount (₹)", "")
        try:
            amount = float(amount_str)
        except ValueError:
            amount = 0.0
        date = st.date_input("Date", value=datetime.today())
        categories = ['Food', 'Home', 'Travel', 'Utilities', 'Entertainment', 'Work', 'Other']
        category = st.selectbox("Category", categories)
        submitted = st.form_submit_button("Add Expense")
        if submitted:
            expense = Expense(
                name=name,
                amount=amount,
                category=category,
                date=date.strftime("%Y-%m-%d")
            )
            write_expense_to_file(expense)
            st.success(f"Added expense: {name}, ₹{amount:.2f}, {category}, {date}")

    st.header("Expense Summary")
    start_date = st.date_input("Start Date", value=datetime.today())
    end_date = st.date_input("End Date", value=datetime.today())

    expenses = read_expenses_from_file(EXPENSE_FILE, start_date, end_date)
    amount_by_category = {}
    for exp in expenses:
        amount_by_category[exp.category] = amount_by_category.get(exp.category, 0) + exp.amount

    if amount_by_category:
        df = pd.DataFrame(list(amount_by_category.items()), columns=["Category", "Total"])
        st.write("### Category-wise Expenses")
        st.table(df)

        st.write("### Expenses by Category (Pie Chart)")
        fig = df.plot.pie(y="Total", labels=df["Category"], autopct="%1.1f%%", legend=False).get_figure()
        st.pyplot(fig)
    else:
        st.write("No expenses found in this date range.")

if __name__ == "__main__":
    main()
