#!/usr/bin/env python3
import matplotlib.pyplot as plt
# from writing import write_transactions_to_csv, view_transactions_from_csv
# import writing

class BudgetTracker:
    def __init__(self):
        self.user = ""
        self.income = 0
        self.expenses = 0
        self.deposits = 0
        self.tx_count = 0
        # self.filename = 'transactions.csv'
        
        # for now the transaction value only is added to this list
        # will add feature later to categorize transactions by user input
        self.each_transaction = []

    # Add a transaction
    def add_one_tx(self):
        self.tx_count += 1
    
    # Subtract a transaction
    def subtract_one_tx(self):
        if self.tx_count > 0:
            self.tx_count -= 1
    
    # Get the number of transactions         
    def get_tx_count(self):
        return self.tx_count
    
    def add_one_deposit(self):
        self.deposits += 1
        
    # Make a deposit subtraction
    def subtract_one_deposit(self):
        if self.deposits > 0:
            self.deposits -= 1
    
    # Get the current number of deposits        
    def get_deposit_count(self):
        return self.deposits
    
    def get_all_transactions(self):
        # format so that the value is set to 2 decimal places in string
        formatted_txs = '; '.join(f'{tx:.2f}' for tx in self.each_transaction)
        print("All transactions entered:", formatted_txs)
        print("Total deposits entered:", self.get_deposit_count())
        print("Total expenses entered:", self.get_tx_count())
        self.view_budget()

    def add_income(self, amount):
        self.income += amount
        self.add_one_deposit()
        self.each_transaction.append(amount)
        # writing.write_transactions_to_csv(self.filename, amount) 
        print("Current number of deposits added:", self.get_deposit_count())
        print(f"Added income: {amount:.2f}")

    def add_expense(self, amount):
        self.expenses += amount
        self.add_one_tx()
        self.each_transaction.append(-1*amount)
        # writing.write_transactions_to_csv(self.filename, -1*amount)
        print(f"Added expense: {amount:.2f}")
        
    # Remove an expense
    def remove_expense(self, amount):
        if self.expenses <= 0 and self.tx_count <= 0:
            print("No expenses to remove. Must have at least one expense recorded.")
            return
        else:
            print(f"Current expenses before removal: {self.expenses:.2f}")
            self.expenses -= amount
            self.subtract_one_tx()
            print(f"Removed expense: {amount:.2f}")
            print("Current number of expenses after removal:", self.get_tx_count())
    
    # Visualize the budget details in bar chart: deposits against expenses
    def view_budget(self):
        print("All budget details:")
        balance = self.income - self.expenses
        print("=========================")
        print("Number of deposits:", self.get_deposit_count())
        print("Number of expenses:", self.get_tx_count())
        print(f"\nTotal Income: {self.income:.2f}")
        print(f"Total Expenses: {self.expenses:.2f}")
        print(f"Current Balance: {balance:.2f}")


    '''
        Visualize the budget using a bar chart
        Returns: bar chart showing income and expenses
    '''
    def visualize_budget_chart(self):
        print("!!! IMPORTANT !!!\n"+
        "Please make sure to close the graph window before continuing use of the tool.")
        print("Now displaying budget chart.")
        plt.figure(figsize=(6, 4))
        plt.bar(['Income', 'Expenses'], [self.income, self.expenses], color=['green', 'red'])
        plt.title('Budget Overview')
        plt.ylabel('Amount ($)')
        plt.xlabel('Category')
        plt.show()

    # def get_csv_file(self):
    #     view_transactions_from_csv(self.filename)

def main():
    
    # initialize an instance of BudgetTracker
    tracker = BudgetTracker()
    # print a welcome message and options to choose from
        
    while True:       
        # the name of this CLI app will be better
        print("\nPersonal Budget Tracker")
        print("=========================================")
        print("Select from one of the following options:")
        print("1. Add a deposit")
        print("2. Add expense")
        print("3. View budget")
        print("4. Get number of transactions")
        print("5. Visualize budget")
        print("6. Enter name")
        # print("7. Generate CSV file of transactions")
        # print("8. Exit") 
        print("7. Exit")
        
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
            tracker.get_all_transactions()
        elif option == '5':
            tracker.visualize_budget_chart()
        elif option == '6':
            name = input("Enter your name: ")
            tracker.user = name
            print(f"Name set to: {tracker.user}")
        # elif option == '7':
        #     tracker.get_csv_file()
        elif option == '7':
            print("Exiting Personal Budget Tracker. Goodbye.")
            break
        

if __name__ == "__main__":
    main()    
