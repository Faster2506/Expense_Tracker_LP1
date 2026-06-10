"""
🔴AI GENERATED COMMENTS:
Project: Personal/Basic Expense Tracker (CLI Version)
Description: A beginner-friendly command-line application to track daily spending,
 manage a monthly budget, search, sort, and export expenses to CSV.
Key Features: Add, view, edit, search, sort, and delete expenses; set monthly budgets;
 generate monthly reports; and export transactions.
Concepts Learned:
  - File I/O and persistent storage using JSON.
  - Exception handling for robust, crash-free user input validation.
  - Data representation using lists of dictionaries.
  - Custom sorting and list manipulation using lambda functions.
  - Exporting structured tabular data to CSV.
"""

import json
import csv
from datetime import date

# --- PERSISTENT DATA INITIALIZATION ---
# Try loading existing data from JSON files. If files do not exist,
# initialize with empty defaults to prevent the program from crashing on startup.
try:
    # Open in read-only mode to load historical expense records.
    with open("expense_tracker_d1.json", "r") as file:
        # Deserialize the JSON string into a Python list of dictionaries.
        Data = json.load(file)
except FileNotFoundError:
    # If the file hasn't been created yet, start with an empty list.
    Data = []

try:
    # Open in read-only mode to load the monthly budget limit.
    with open("expense_budget.json", "r") as file1:
        Budget = json.load(file1)
except FileNotFoundError:
    # Default budget structure when no budget has been set yet.
    Budget = {
        "Budget": 0
    }

# --- HELPER FUNCTIONS ---
# Centralizing saving logic in a helper function adheres to the DRY (Don't Repeat Yourself)
# principle, ensuring that file writes are handled consistently across all CRUD operations.
def save_data():
    # Open file in write mode ('w') to overwrite with the updated state.
    with open("expense_tracker_d1.json", "w") as file:
        # Serialize the Python list of dictionaries into formatted JSON with indentation.
        json.dump(Data, file, indent=4)

# Defining a return value allows this utility function to be reused flexibly
# throughout the app (e.g., in both the budget comparison and general statistics options).
def calculate_total_spending():
    total_spending = 0
    # Iterate through the list of expenses to accumulate the sum of amounts.
    for expense in Data:
        total_spending += expense["Amount"]
    return total_spending

# --- INITIAL APP GREETING FLOW ---
print("Welcome🙏, would you like to Calculate your EXPENSES?💸..(y/n)")

Reply = input()

if Reply != "y":
    print("Okay, have a nice day!")
    exit()

print("GREAT Let's get started:")

# --- MAIN MENU LOOP ---
while True:
    choice = input(
                "\nWhat would you like to do?\n"
                "1. ➕ Add an expense\n" 
                "2. 👀 View expenses\n"
                "3. ✍️ Edit expenses\n"
                "4. 🔴 Delete expense\n"
                "5. 💰 Total Spending And Number of Expenses\n"
                "6. 🔎 Search Any Expense\n"
                "7. 🎯 Set Monthly Budget\n"
                "8. 📊 View Monthly Budget\n"
                "9. 🗓️ Monthly Expense Report\n"
                "10.📈 Highest Expense\n"
                "11.📉 Lowest Expense\n"
                "12.✅ Sort Expense\n"
                "13.📃 Export Expense to CSV\n"
                "14.🏃🏻Exit:\n"
                "Enter choices: "
    )

    # ------------------------------------------
    # CHOICE 1: ADD AN EXPENSE (CREATE)
    # ------------------------------------------
    if choice == "1":
        expense_name = input("Enter your Expense Name: ").title()
        expense_category = input("Enter you Expense Category: ").title()
    
        # Use a try-except block to gracefully catch non-numeric inputs (like letters)
        # which would otherwise cause float() conversion to raise a ValueError and crash the app.
        try:           
            expense_amount = float(input("ENTER THE AMOUNT: "))
            expense_data = {
                "Name": expense_name,
                "Amount": expense_amount,
                "Category": expense_category,
                "Date": str(date.today())  # Auto-capture the current system date in YYYY-MM-DD format
            }
            Data.append(expense_data)
            save_data()  # Persist changes immediately to file
            
            print("Expense added successfully!✅")
            
        except ValueError:
            print("❌Please enter a valid number!!")

    # ------------------------------------------
    # CHOICE 2: VIEW EXPENSES (READ)
    # ------------------------------------------
    elif choice == "2":
        print("\nYour Expenses: ")
        
        # enumerate() is used to print 1-based index numbers along with each expense,
        # giving the user a clear reference number for editing or deleting records.
        for index, expense in enumerate(Data, start=1):
            print(f"\n📌 Expense #{index}\n")
            print(f"👤 Name     : {expense['Name']}")
            print(f"💰 Amount   : ₹{expense['Amount']}")
            print(f"🏷️ Category : {expense['Category']}")
            print(f"📆 Date     : {expense['Date']}")
            print("-----------------------------")           

    # ------------------------------------------
    # CHOICE 3: EDIT EXPENSES (UPDATE)
    # ------------------------------------------
    elif choice == "3":
        # Display index numbers to help the user choose the right item.
        for index, expense in enumerate(Data, start = 1):
            print(f"{index}. {expense['Name']}👤 -> ₹{expense['Amount']} 💰")
        try:
            expense_number = int(input("Enter the number of the expense you want to edit: "))
            
            # Guard clause: ensure user input is within the actual boundaries of the Data list.
            if expense_number < 1 or expense_number > len(Data):
                print("❌ Invalid expense number......")
                continue
            
            # Convert 1-based UI number back to 0-based Python list index.
            expense_index = expense_number - 1

            new_name = input("Enter new expense name: ").title()
            new_amount = float(input("Enter new amount: "))
            new_category = input("Enter new category: ").title()
            
            # Update the dictionary properties in-place.
            Data[expense_index]["Name"] = new_name
            Data[expense_index]["Amount"] = new_amount
            Data[expense_index]["Category"] = new_category
            
            save_data()  # Persist modifications to JSON
            
            print("Expense updated successgully!✅")
            
        except ValueError:
            print("❌Please Enter a Valid Number!")
            
    # ------------------------------------------
    # CHOICE 4: DELETE EXPENSE (DELETE)
    # ------------------------------------------
    elif choice == "4":
        # Display items with reference indexes.
        for index, expense in enumerate(Data, start = 1):
            print(f"{index}. {expense['Name']}👤 -> ₹{expense['Amount']} 💰")
        try:
            expense_number = int(input("Which expense would you like to DELETE?🔴"))
        
            # Convert UI selection to Python 0-based list index.
            expense_index = expense_number - 1
        
            # pop() removes and returns the item at the specified index, updating the list in memory.
            deleted_expense = Data.pop(expense_index)
            save_data()  # Save the updated list back to file
            
            print(f"{deleted_expense['Name']} deleted successfully!✅")    
            
        except IndexError:
            # Handles inputs out of range, preventing index out of bounds exceptions.
            print("❌ Expense number doesn't exist.")
            
    # ------------------------------------------
    # CHOICE 5: TOTAL SPENDING AND COUNT (STATS)
    # ------------------------------------------
    elif choice == "5":
        # Calculate statistics using the helper function and the built-in len() function.
        total_spending  = calculate_total_spending()
            
        print(f"💰 Total Spending: ₹{total_spending}")
        print(f"🗓️ Number of Expenses: {len(Data)}")
        
    # ------------------------------------------
    # CHOICE 6: SEARCH ANY EXPENSE (SEARCH)
    # ------------------------------------------
    elif choice == "6":
        search_expense = input("Enter Your Expense name: ").lower()
        
        found = False
        
        # Perform a sequential linear search to locate the first matching expense name.
        for expense in Data:
            # Cast both names to lowercase to make the search case-insensitive.
            if expense["Name"].lower() == search_expense:
                found = True
                
                print("\n📌 Expense Found\n")
                print(f"👤 Name     : {expense['Name']}")
                print(f"💰 Amount   : ₹{expense['Amount']}")
                print(f"🏷️ Category : {expense['Category']}")
                print(f"📆 Date     : {expense['Date']}")
                
                break  # Exit the loop immediately after finding the first match
        
        if not found:
            print("❌ Expense Not Found...")
    
    # ------------------------------------------
    # CHOICE 7: SET MONTHLY BUDGET (BUDGET SET)
    # ------------------------------------------
    elif choice == "7":
        print("Let's Set a Monthly Budget For you!!🎯")
        try:
            monthly_budget = float(input("Enter your Monthly budget: "))
            
            # Store budget configuration in a dictionary and persist it to a separate JSON file.
            budget_data = {
                "Budget": monthly_budget,
            }
            Budget = budget_data
            
            with open("expense_budget.json", "w") as file1:
                json.dump(budget_data, file1, indent=4)
            
            print(f"Budget of ₹{monthly_budget} is now locked!!🔒")
            
        except ValueError:
            print("Please enter a valid Budget!!🙂")
            
    # ------------------------------------------
    # CHOICE 8: VIEW MONTHLY BUDGET (BUDGET VIEW)
    # ------------------------------------------
    elif choice == "8":
        monthly_budget = Budget["Budget"]
        total_spending = calculate_total_spending()
        remaining_budget = monthly_budget - total_spending
        
        print(f"\n🎯 Monthly Budget : ₹{monthly_budget}")
        print(f"💸 Total Spent      : ₹{total_spending}")
        
        # Display visual budget alerts depending on whether spending exceeds the budget threshold.
        if remaining_budget >= 0: 
            print(f"💰 Remaining Budget : ₹{remaining_budget}")
        else:
            print(f"⚠️ Budget Exceeded By ₹{-remaining_budget}")
    
    # ------------------------------------------
    # CHOICE 9: MONTHLY REPORT (REPORT FILTER)
    # ------------------------------------------
    elif choice == "9":
        try:
            # Query format should match 'YYYY-MM'
            month = input("Enter month (YYYY-MM): ")
            monthly_total = 0
            monthly_expense = 0
            
            print(f"\n🗓️ {month} Report")
            print(f"\n📌 Expenses Included: ")
            
            # Filter and display all expenses matching the queried month sequence.
            for expense in Data:
                # Dates are strings formatted as 'YYYY-MM-DD'. Splice [0:7] extracts the 'YYYY-MM' portion.
                if expense["Date"][0:7] == month:
                    monthly_total += expense["Amount"]
                    monthly_expense += 1
                    
                    print(f"• {expense['Name']} - ₹{expense['Amount']}")
                    
            if monthly_expense == 0:
                print("❌ No expense found!!")
                
            else:
                print(f"\n💰 Total Spending : ₹{monthly_total}")
                print(f"🗓️ Total Expense  :  {monthly_expense}")
                
        except ValueError:
            print("❌Enter  valid Date!!")
    
    # ------------------------------------------
    # CHOICE 10: HIGHEST EXPENSE (MAX ANALYTICS)
    # ------------------------------------------
    elif choice == "10":
        # max() uses a lambda function to extract and compare the "Amount" key of each dictionary.
        highest_expense = max(Data, key=lambda expense: expense["Amount"])
        
        print(f"🏆 Highest Expense ")
        print(f"👤 Name       : {highest_expense['Name']}")
        print(f"💰 Amount     : {highest_expense['Amount']}")
        print(f"🏷️ Category    : {highest_expense['Category']}")
        print(f"📆 Date       : {highest_expense['Date']}")
        
    # ------------------------------------------
    # CHOICE 11: LOWEST EXPENSE (MIN ANALYTICS)
    # ------------------------------------------
    elif choice == "11":
        # min() uses a lambda function to find the record with the minimum "Amount" value.
        lowest_expense = min(Data, key=lambda expense: expense["Amount"])
        
        print(f"📉 Lowest Expense ")
        print(f"👤 Name       : {lowest_expense['Name']}")
        print(f"💰 Amount     : {lowest_expense['Amount']}")
        print(f"🏷️ Category    : {lowest_expense['Category']}")
        print(f"📆 Date       : {lowest_expense['Date']}")
        
    # ------------------------------------------
    # CHOICE 12: SORT EXPENSES (SORTING)
    # ------------------------------------------
    elif choice == "12":
        print("\n1. HIGHEST TO LOWEST")
        print("2. LOWEST TO HIGHEST")
        
        sort_choice = input("Enter choice:")
        
        # Use sorted() with lambdas to generate a new ordered list, keeping original data intact.
        if sort_choice == "1":
            sorted_expenses = sorted(
                Data,
                key = lambda expense: expense["Amount"],
                reverse = True  # Sorts descending
            )
            
        elif sort_choice == "2":
            sorted_expenses = sorted(
                Data,
                key=lambda expense: expense["Amount"]  # Sorts ascending
            )
            
        else:
            print("❌ Invalid choice.")
            continue
            
        print("\n✅ Sorted Expenses\n")
        
        for expense in sorted_expenses:
            print(f"👤 Name     : {expense['Name']}")
            print(f"💰 Amount   : ₹{expense['Amount']}")
            print(f"🏷️ Category : {expense['Category']}")
            print(f"📆 Date     : {expense['Date']}")
            print("-----------------------------")
        
    # ------------------------------------------
    # CHOICE 13: EXPORT EXPENSES (CSV GENERATOR)
    # ------------------------------------------
    elif choice == "13":
        if not Data:
            print("❌ No expenses to export.")
            continue
        
        # open with newline="" prevents blank lines from being inserted between rows in Windows environments.
        with open("expenses.csv", "w", newline="") as file:
            writer = csv.writer(file)
            
            # Write column header names first.
            writer.writerow(["Name", "Amount", "Category", "Date"])
            
            # Write data rows sequentially.
            for expense in Data:
                writer.writerow([
                    expense["Name"],
                    expense["Amount"],
                    expense["Category"],
                    expense["Date"]
                ])
                
        print("✅ Expenses exported to expense.csv successfully!")
        
    # ------------------------------------------
    # CHOICE 14: EXIT APPLICATION
    # ------------------------------------------
    elif choice == "14":
        print("Goodbye....🤝🏻")
        break

    else:
        print("Invalid choice. Try AGAIN.")