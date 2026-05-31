import json
from datetime import date

try:
    with open("expense_tracker_d1.json", "r") as file:
        Data = json.load(file)
except FileNotFoundError:
    Data=[]

try:
    with open("expense_budget.json", "r") as file1:
        Budget = json.load(file1)
except FileNotFoundError:
    Budget = {
        "Budget": 0
    }
        
print("Welcome🙏, would you like to Calculate your EXPENSES?💸..(y/n)")

def save_data():
    with open("expense_tracker_d1.json", "w") as file:
        json.dump(Data, file, indent=4)

def calculate_total_spending():
    
    total_spending = 0
    
    for expense in Data:
        total_spending += expense["Amount"]

    return total_spending

Reply = input()

if Reply != "y":
    print("Okay, have a nice day!")
    exit()

print("GREAT Let's get started:")

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
                "9. 🏃🏻Exit:\n"
                "Enter choices: "
    )

    if choice == "1":
        
        expense_name = input("Enter your Expense Name: ").title()
        expense_category = input("Enter you Expense Category: ").title()
    
        try:           
            expense_amount = float(input("ENTER THE AMOUNT: "))
            expense_data = {
                "Name": expense_name,
                "Amount": expense_amount,
                "Category": expense_category,
                "Date": str(date.today())
            }
            Data.append(expense_data)
            save_data()
            
            print("Expense added successfully!✅")
            
        except ValueError:
            print("❌Please enter a valid number!!")

    elif choice == "2":
        print("\nYour Expenses: ")
        
        for index, expense in enumerate(Data, start=1):
            print(f"\n📌 Expense #{index}\n")
            
            print(f"👤 Name     : {expense["Name"]}")
            print(f"💰 Amount   : ₹{expense["Amount"]}")
            print(f"🏷️ Category : {expense["Category"]}")
            print(f"📆 Date     : {expense["Date"]}")
            
            print("-----------------------------")           
    elif choice == "3":

        for index, expense in enumerate(Data, start = 1):
            print(f"{index}. {expense['Name']}👤 -> ₹{expense['Amount']} 💰")
        try:
            expense_number = int(input("Enter the number of the expense you want to edit: "))
            
            if expense_number < 1 or expense_number>len(Data):
                print("❌ Invalid expense number......")
                continue
            
            expense_index = expense_number - 1

            new_name = input("Enter new expense name: ").title()
            new_amount = float(input("Enter new amount: "))
            new_category = input("Enter new category: ").title()
            
            Data[expense_index]["Name"] = new_name
            Data[expense_index]["Amount"] = new_amount
            Data[expense_index]["Category"] = new_category
            
            save_data()
            
            print("Expense updated successgully!✅")
            
        except ValueError:
            print("❌Please Enter a Valid Number!")
            
    elif choice == "4":
        
        for index, expense in enumerate(Data, start = 1):
            print(f"{index}. {expense["Name"]}👤 -> ₹{expense["Amount"]} 💰")
        try:
            expense_number = int(input("Which expense would you like to DELETE?🔴"))
        
            expense_index = expense_number - 1
        
            deleted_expense = Data.pop(expense_index)
            
            save_data()
            
            print(f"{deleted_expense["Name"]} deleted successfully!✅")    
            
        except IndexError:
            print("❌ Expense number doesn't exist.")
            
    elif choice == "5":
        
        total_spending  = calculate_total_spending()
            
        print(f"💰 Total Spending: ₹{total_spending}")
        print(f"🗓️ Number of Expenses: {len(Data)}")
        
    elif choice =="6":
        search_expense = input("Enter Your Expense name: ").lower()
        
        found = False
        
        for expense in Data:
            
            if expense["Name"].lower() == search_expense:
                
                found = True
                
                print("\n📌 Expense Found\n")
                print(f"👤 Name     : {expense["Name"]}")
                print(f"💰 Amount   : ₹{expense["Amount"]}")
                print(f"🏷️ Category : {expense["Category"]}")
                print(f"📆 Date     : {expense["Date"]}")
                
                break
        
        if not found:
            print("❌ Expense Not Found...")
    
    elif choice == "7":
        print("Let's Set a Monthly Budget For you!!🎯")
        try:
            monthly_budget = float(input("Enter your Monthly budget: "))
            
            budget_data = {
                "Budget": monthly_budget,
            }
            Budget = budget_data
            
            with open("expense_budget.json", "w") as file1:
                json.dump(budget_data, file1, indent=4)
            
            print(f"Budget of ₹{monthly_budget} is now locked!!🔒")
            
        except ValueError:
            print("Please enter a valid Budget!!🙂")
            
    elif choice == "8":
        monthly_budget = Budget["Budget"]
        
        total_spending = calculate_total_spending()
        
        remaining_budget = monthly_budget - total_spending
        
        print(f"\n🎯 Monthly Budget : ₹{monthly_budget}")
        print(f"💸 Total Spent      : ₹{total_spending}")
        
        if remaining_budget >=0: 
            print(f"💰 Remaining Budget : ₹{remaining_budget}")
        else:
            print(f"⚠️ Budget Exceeded By ₹{-remaining_budget}")
            
    elif choice == "9":

        print("Goodbye....🤝🏻")
        break

    else:

        print("Invalid choice. Try AGAIN.")