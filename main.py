import json

try:
    with open("expense_tracker_d1.json", "r") as file:
        Data = json.load(file)
except FileNotFoundError:
    Data=[]
    
print("Welcome🙏, would you like to Calculate your EXPENSES?💸..(y/n)")

def save_data():
    with open("expense_tracker_d1.json", "w") as file:
        json.dump(Data, file, indent=4)

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
                "6. 🏃🏻Exit:\n"
                "Enter choices: "
    )

    if choice == "1":
        
        expense_name = input("Enter your Expense Name: ")
        expense_category = input("Enter you Expense Category: ")
        
        try:           
            expense_amount = float(input("ENTER THE AMOUNT: "))
            expense_data = {
                "Name": expense_name,
                "Amount": expense_amount,
                "Category": expense_category,
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

            new_name = input("Enter new expense name: ")
            new_amount = float(input("Enter new amount: "))
            new_category = input("Enter new category: ")
            
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
        total_spending = 0
        
        for expense in Data:
            total_spending += expense["Amount"]
            
        print(f"💰 Total Spending: ₹{total_spending}")
        print(f"🗓️ Number of Expenses: {len(Data)}")
        
    elif choice == "6":

        print("Goodbye....🤝🏻")
        break

    else:

        print("Invalid choice. Try AGAIN.")