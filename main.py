Data = []

print("Welcome, would you like to Calculate your EXPENSES?..(y/n)")

Reply = input()

if Reply != "y":
    print("Okay, have a nice day!")
    exit()

print("GREAT Let's get started:")

while True:
    
    choice = input(
                "\nWhat would you like to do?\n"
                "1. add an expense\n" 
                "2. view expenses\n"
                "3. exit:\n"
                "Enter choices: "
    )

    if choice == "1":
        expense_name = input("Enter your Expense Name: ")
        expense_amount = float(input("ENTER THE AMOUNT: "))
        expense_data = {
            "Name": expense_name,
            "Amount": expense_amount
        }

        Data.append(expense_data)

        print("Expense added successfully!!")

    elif choice == "2":
        print("\nYour Expenses: ")
        
        for expense in Data:
            print(expense)

    elif choice =="3":

        print("Goodbye....")
        break

    else:

        print("Invalid choice. Try AGAIN.")