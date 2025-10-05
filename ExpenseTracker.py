from expense import Expense
from datetime import datetime

def main():
    print("Welcome to Expense Tracker")
    expense_file_path = "expenses.csv"

    # Allow the user to add multiple expenses
    while True:
        ans = input("Add another expense? (y/n): ").lower()
        if ans == "y":
            expense = get_expense_details()
            write_expense_to_file(expense, expense_file_path)
        else:
            break

    # Input for summary filtering
    start_date_str = input("Enter start date (YYYY-MM-DD): ")
    end_date_str = input("Enter end date (YYYY-MM-DD): ")
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

    # Summarize and display results
    read_expenses_from_file(expense_file_path, start_date, end_date)

def get_expense_details():
    print("Enter expense details")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))
    date_input = input("Enter expense date (YYYY-MM-DD) or leave empty for today: ")
    if not date_input:
        date_input = datetime.today().strftime('%Y-%m-%d')

    expense_categories = [
        'Food',
        'Home',
        'Travel',
        'Utilities',
        'Entertainment',
        'Work',
        'Other'
    ]

    while True:
        print("Select a category from the following:")
        for i, category_name in enumerate(expense_categories):
            print(f" {i+1}. {category_name}")

        value_range = f"[1-{len(expense_categories)}]"
        try:
            selected_index = int(input(f"Enter your choice {value_range}: ")) - 1
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(
                name=expense_name,
                category=selected_category,
                amount=expense_amount,
                date=date_input
            )
            return new_expense
        else:
            print("Invalid choice. Please try again.")

def write_expense_to_file(expense: Expense, expense_file_path):
    print(f"Writing expense to file: {expense} to {expense_file_path}")
    with open(expense_file_path, 'a') as f:
        f.write(f"{expense.name},{expense.amount},{expense.category},{expense.date}\n")

def read_expenses_from_file(expense_file_path, start_date, end_date):
    print("Reading expenses from file")
    expenses = []
    with open(expense_file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            parts = line.strip().split(',')
            if len(parts) == 4:
                expense_name, expense_amount, expense_category, expense_date = parts
            else:
                continue  # Skip malformed lines

            try:
                expense_dt = datetime.strptime(expense_date, "%Y-%m-%d").date()
            except ValueError:
                continue  # Skip or handle invalid date format

            if start_date <= expense_dt <= end_date:
                line_expense = Expense(
                    name=expense_name,
                    amount=float(expense_amount),
                    category=expense_category,
                    date=expense_date
                )
                expenses.append(line_expense)

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        amount_by_category[key] = amount_by_category.get(key, 0) + expense.amount

    for key, amount in amount_by_category.items():
        print(f"Total expense for {key}: ₹{amount:.2f}")

if __name__ == "__main__":
    main()
