from datetime import datetime

date_format = "%d-%m-%Y"
CATERGORY_OPTIONS = {"I": "Income", "E": "Expense"}

# Function to get a valid date from the user
# This function will keep asking for a date until a valid one is provided
def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)
    
    try:
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid date format. Please enter the date in the format dd-mm-yyyy.")
        return get_date(prompt, allow_default)

# Function to get a valid amount from the user
# This function will keep asking for an amount until a valid one is provided
def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be a non-negative non-zero value.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()
    

# Function to get a valid category from the user
# This function will keep asking for a category until a valid one is provided
def get_category():
    category = input("Enter the category ('I' for income, 'E' for expense):  ").upper()
    if category in CATERGORY_OPTIONS:
        return CATERGORY_OPTIONS[category]
    
    print("Invalid category. Please enter 'I' for income or 'E' for expense.")
    return get_category()


# Function to get a valid description from the user
# This function will keep asking for a description until a valid one is provided
def get_description():
    return input("Enter a description(optional): ")
    

