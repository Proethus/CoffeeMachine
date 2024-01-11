import math


def refill_resources():
    for item in ["Water", "Coffee", "Milk"]:
        resources[item] += int(input(f"How much {item.lower()} would you like to add? "))
    for a_coin in [1, 5, 10, 25]:
        resources["Coins"][coin] += int(input(f"How many {a_coin}-cent coins would you like to add? "))


def calculate_coins_value(coins):
    return sum(a_coin * coins[coin] for a_coin in coins) * 0.01


def report():
    print("Current resources:")
    for item, amount in resources.items():
        if item == "Coins":
            print(f"Money: ${calculate_coins_value(amount)}")
            for a_coin, a_amount in resources["Coins"].items():
                print(f"You have {a_amount} pcs of ${a_coin*0.01}")
        else:
            print(f"{item}: {amount} {'ml' if item in ['Water', 'Milk'] else 'g'}")


def check_coffee_resources(coffee):
    return all(resources[item] >= coffee[item] for item in ["Water", "Coffee", "Milk"])


def make_coffee(coffee):
    for item in ["Water", "Coffee", "Milk"]:
        resources[item] -= coffee[item]


def process_order():
    money_paid = calculate_coins_value(order["Coins"])
    if money_paid < order["Price"]:
        print("Insufficient funds! Abort transaction")
    else:
        if not check_coffee_resources(order):
            print("Insufficient materials! Aborting transaction!")
        else:
            for a_coin, amount in order["Coins"].items():
                resources["Coins"][a_coin] += amount
            make_coffee(order)
            change = money_paid - order["Price"]
            for a_coin in [25, 10, 5, 1]:
                if change > a_coin * 0.01:
                    removable_coin_amount = math.floor(change / (a_coin * 0.01))
                    if resources["Coins"][a_coin] > removable_coin_amount:
                        change -= removable_coin_amount * a_coin
                        resources["Coins"][a_coin] -= removable_coin_amount
            if change > 0:
                print("The machine ran out of change. Sorry for the inconvenience!")
            print(f"Enjoy your coffee!")


coffee_types = {"Espresso": {"Water": 50, "Coffee": 18, "Milk": 0, "Price": 1.50},
                "Latte": {"Water": 200, "Coffee": 24, "Milk": 150, "Price": 2.50},
                "Cappuccino": {"Water": 50, "Coffee": 24, "Milk": 100, "Price": 3.00}}
resources = {"Water": 300, "Milk": 200, "Coffee": 100, "Coins": {1: 0, 5: 0, 10: 0, 25: 0}}
order = {"Water": 0, "Coffee": 0, "Milk": 0, "Price": 0}
finished = False

while not finished:
    order_name = input("Please select a product: Espresso, Latte, Cappuccino: ")

    if order_name == "report":
        report()
    elif order_name == "refill":
        refill_resources()
    elif order_name in coffee_types:
        order = coffee_types[order_name].copy()
        order["Coins"] = {25: 0, 10: 0, 5: 0, 1: 0}
        done = False
        while not done:
            for coin in order["Coins"]:
                order["Coins"][coin] = int(input(f"How many ${coin*0.01} would you like to insert?"))
            done = input("Would you like to insert more coins? yes or no?") == "no"

        process_order()
    else:
        print("Incorrect order! Please try again!")
    finished = input("Would you like another coffee? yes or no") == "no"
