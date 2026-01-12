#!/usr/bin/env python3
import matplotlib.pyplot as plt

class BudgetTracker:
    def __init__(self):
        self.user = ""
        self.income = 0
        self.expenses = 0

    def add_income(self, amount):
        self.income += amount
        print(f"Added income: ${amount:.2f}")

    def add_expense(self, amount):
        self.expenses += amount
        print(f"Added expense: ${amount:.2f}")

    def view_budget(self):
        balance = self.income - self.expenses
        print(f"\nTotal Income: ${self.income:.2f}")
        print(f"Total Expenses: ${self.expenses:.2f}")
        print(f"Current Balance: ${balance:.2f}")

    def visualize_budget(self):
        plt.figure(figsize=(6, 4))
        plt.bar(['Income', 'Expenses'], [self.income, self.expenses], color=['green', 'red'])
        plt.title('Budget Overview')
        plt.ylabel('Amount ($)')
        plt.show()


def main():
    
    # initialize an instance of BudgetTracker
    tracker = BudgetTracker()
    # print a welcome message and options to choose from
    tracker.user = input("Enter your name to start the Budget Tracker: ")
    print(f"Welcome, {tracker.user}!\n") 
    
    while True:       
        # the name of this CLI app will be better
        print("\nPersonal Budget Tracker\n")
        print("Select from one of the following options:")
        print("1. Add to income")
        print("2. Add expense")
        print("3. View budget")
        print("4. Visualize budget")
        print("5. Exit")
        
        # the option menu and input system
        option = input("Enter your choice here: ")
        if option == '1':
            amount = float(input("Enter income amount: $"))
            tracker.add_income(amount)
        elif option == '2':
            amount = float(input("Enter expense amount: $"))
            tracker.add_expense(amount)
        elif option == '3':
            tracker.view_budget()
        elif option == '4':
            tracker.visualize_budget()
        elif option == '5':
            print("Exiting Budget Tracker. Goodbye!")
            break
        

if __name__ == "__main__":
    main()    
