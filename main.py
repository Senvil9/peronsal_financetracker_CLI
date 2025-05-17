import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date, get_amount, get_category, get_description
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMN_NAMES = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

#DataFrame - Object within Pandas that allows us to access difffernt rows/columns from a CSV file
    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMN_NAMES)
            df.to_csv(cls.CSV_FILE, index=False)
    
    @classmethod
    def add_entry(cls, date, amount, category, description):
        #Store in Python dictionary    
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        #Context manager and automatically closes the file
        #Open the CSV file in append mode
        #newline='' prevents blank lines from being added
        with open(cls.CSV_FILE, mode='a', newline='') as csvfile:
            # Take a dictionary and write it to a CSV file
            writer = csv.DictWriter(csvfile, fieldnames = cls.COLUMN_NAMES)
            writer.writerow(new_entry)
        print("Entry added successfully.")

    @classmethod
    #Give us all the transactions in the CSV file with in the date range
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        #Convert all the dates in the CSV file to datetime objects use to get different transactions
        df["date"] = pd.to_datetime(df["Date"], format=CSV.FORMAT) # Sort by Correct Date
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]
        
        if filtered_df.empty:
            print("No transactions found in the specified date range.")
        else:
            print(
                f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}:"
                )
            print(
                filtered_df.to_string(
                    index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}
                    )
                )

            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print("\nSummary:")
            print(f"Total Income: ${total_income}")
            print(f"Total Expense: ${total_expense}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")
        return filtered_df
        


#Writing a function that will call these function in the order that we want
def add():
    # Get user input
    CSV.initialize_csv()
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    # Add entry to CSV
    CSV.add_entry(date, amount, category, description)

def plot_transactions(df):
    df.set_index("date", inplace = True)
    
    income_df = (
        df[df["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
        
    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="green")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="red")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expense Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to plot the transactions? (y/n): ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting ....")
            break
        else:
            print("Invalid choice. Please enter a number between 1, 2 or 3.")

if __name__ == "__main__":
    main()
#This is the main file that will run the program
        