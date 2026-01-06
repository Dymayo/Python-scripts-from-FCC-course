class Category:
    def __init__(self, name):
        self.name = name
        self.ledger= []

    def deposit(self,amount,description=""):
        self.ledger.append({'amount': amount, 'description': description})

    def withdraw(self,amount,description=""):
        if self.check_funds(amount):
            self.ledger.append({'amount': -amount, 'description': description})
            return True
        return False
    
    
    def get_balance(self):
        return sum(txn['amount'] for txn in self.ledger)

    def transfer(self,amount,category):
        if (self.check_funds(amount)):
            self.withdraw(amount,f"Transfer to {category.name}")
            category.deposit(amount,f"Transfer from {self.name}")
            return True
        return False


    def check_funds(self,amount):
        if amount> self.get_balance():
            return False
        return True

    def __str__(self):
        title = self.name.center(30, "*") + "\n"

        lines = ""
        for txn in self.ledger:
            desc = txn["description"][:23].ljust(23)          
            amt = f"{txn['amount']:.2f}".rjust(7)     
            lines += f"{desc}{amt}\n"

        total = f"Total: {self.get_balance():.2f}"
        return title + lines + total
        

def create_spend_chart(categories):
    title = "Percentage spent by category\n"

    amounts = []
    total_amount = 0
    for category in categories:
        spent = 0
        for txn in category.ledger:
            if txn["amount"] < 0:
                spent += -txn["amount"]
        amounts.append(spent)
        total_amount += spent

    percentages = [int(amount / total_amount * 100) // 10 * 10 for amount in amounts]

    lines_chart = ""
    for percentage in range(100, -1, -10):
        line = f"{percentage:>3}| "
        for e in percentages:
            if e >= percentage:
                line += "o  "
            else:
                line += "   "
        lines_chart += line + "\n"

    separator = "    " + "-" * (3 * len(categories) + 1) + "\n"

    max_len = max(len(category.name) for category in categories)
    labels = ""
    for i in range(max_len):
        labels += "     " 
        for category in categories:
            if i < len(category.name):
                labels += category.name[i] + "  "
            else:
                labels += "   "
        labels += "\n"

    return title + lines_chart + separator + labels.rstrip("\n")


food = Category("Food")
food.deposit(1000)
food.withdraw(105.55)

clothing = Category("Clothing")
clothing.deposit(500)
clothing.withdraw(50)

auto = Category("Auto")
auto.deposit(1000)
auto.withdraw(25)

print(create_spend_chart([food, clothing, auto]))
