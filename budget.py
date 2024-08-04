class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        return sum(item["amount"] for item in self.ledger)

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        return self.get_balance() >= amount

    def __str__(self):
        title = f"{self.name:*^30}\n"
        items = ""
        for item in self.ledger:
            items += f"{item['description'][:23]:23}{item['amount']:>7.2f}\n"
        total = self.get_balance()
        return title + items + f"Total: {total:.2f}"


def create_spend_chart(categories):
    # Calculate total spent per category
    total_spent = sum(sum(-item['amount'] for item in cat.ledger if item['amount'] < 0) for cat in categories)
    category_spent = [(cat.name, sum(-item['amount'] for item in cat.ledger if item['amount'] < 0)) for cat in categories]
    percentages = [(name, int(spent / total_spent * 100)) for name, spent in category_spent]

    # Create the chart
    chart = "Percentage spent by category\n"
    for i in range(100, -1, -10):
        chart += f"{i:>3}| "
        for _, percent in percentages:
            chart += "o  " if percent >= i else "   "
        chart += "\n"
    
    chart += "    -" + "---" * len(categories) + "\n"
    
    # Create the labels
    max_length = max(len(cat.name) for cat in categories)
    names = [cat.name.ljust(max_length) for cat in categories]
    
    for i in range(max_length):
        chart += "     "
        for name in names:
            chart += name[i] + "  "
        chart += "\n"

    return chart.rstrip("\n")


# Example Usage
food = Category("Food")
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")
clothing = Category("Clothing")
food.transfer(50, clothing)
print(food)

clothing.deposit(500, "initial deposit")
clothing.withdraw(75, "jacket")
clothing.withdraw(25, "shoes")
print(clothing)

entertainment = Category("Entertainment")
entertainment.deposit(100, "initial deposit")
entertainment.withdraw(50, "movie night")
print(entertainment)

print(create_spend_chart([food, clothing, entertainment]))

