import tkinter as tk
from tkinter import messagebox
import random
import datetime

stocks = {
    "Apple": {"price": 150, "owned": 0},
    "Google": {"price": 2800, "owned": 0},
    "Tesla": {"price": 700, "owned": 0}
}
balance = 10000
transactions = []

market_events = [
    ("Great earnings report!", 1.1),
    ("Product recall announced!", 0.9),
    ("New government policy affects tech stocks.", 0.95),
    ("Market surge due to investor confidence!", 1.05),
    ("Economic downturn warning!", 0.92)
]

def update_prices():
    global stocks
    event = random.choice(market_events)
    multiplier = event[1]
    for stock in stocks:
        change = random.uniform(-5, 5) * multiplier
        stocks[stock]["price"] = round(max(1, stocks[stock]["price"] + change), 2)
    update_display()
    messagebox.showinfo("Market News", f"{event[0]}\nPrices have been adjusted.")

def buy_stock(stock):
    global balance
    try:
        quantity = int(quantity_entries[stock].get())
        if quantity <= 0:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Invalid Input", "Enter a valid number of shares.")
        return
    price = stocks[stock]["price"] * quantity
    if balance >= price:
        stocks[stock]["owned"] += quantity
        balance -= price
        transactions.append(f"{datetime.datetime.now()}: Bought {quantity} {stock} @ ${stocks[stock]['price']:.2f}")
        update_display()
    else:
        messagebox.showwarning("Insufficient Funds", "You don't have enough money!")

def sell_stock(stock):
    global balance
    try:
        quantity = int(quantity_entries[stock].get())
        if quantity <= 0:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Invalid Input", "Enter a valid number of shares.")
        return
    if stocks[stock]["owned"] >= quantity:
        stocks[stock]["owned"] -= quantity
        balance += stocks[stock]["price"] * quantity
        transactions.append(f"{datetime.datetime.now()}: Sold {quantity} {stock} @ ${stocks[stock]['price']:.2f}")
        update_display()
    else:
        messagebox.showwarning("Not Enough Shares", f"You don't own {quantity} {stock} shares!")

def update_display():
    balance_label.config(text=f"Balance: ${balance:.2f}")
    for stock in stocks:
        price_labels[stock].config(text=f"Price: ${stocks[stock]['price']}")
        owned_labels[stock].config(text=f"Owned: {stocks[stock]['owned']}")
    update_portfolio_value()

def update_portfolio_value():
    total = balance
    for stock in stocks:
        total += stocks[stock]['price'] * stocks[stock]['owned']
    portfolio_label.config(text=f"Total Portfolio Value: ${total:.2f}")

    if total > 10000:
        status_label.config(text="🟢 You are currently in a profit situation", fg="green")
    elif total < 10000:
        status_label.config(text="🔴 You are currently in a loss situation", fg="red")
    else:
        status_label.config(text="⚪ No gain or loss yet", fg="gray")

def show_transaction_log():
    log_window = tk.Toplevel(root)
    log_window.title("Transaction Log")
    text = tk.Text(log_window, height=20, width=60)
    text.pack()
    for t in transactions:
        text.insert(tk.END, t + "\n")

root = tk.Tk()
root.title("Virtual Stock Market Simulator")

balance_label = tk.Label(root, text=f"Balance: ${balance:.2f}", font=("Helvetica", 14))
balance_label.pack()

frame = tk.Frame(root)
frame.pack(pady=10)

price_labels = {}
owned_labels = {}
quantity_entries = {}

for stock in stocks:
    stock_frame = tk.Frame(frame, pady=5)
    stock_frame.pack()

    tk.Label(stock_frame, text=stock, font=("Helvetica", 12, "bold")).grid(row=0, column=0)

    price_labels[stock] = tk.Label(stock_frame, text=f"Price: ${stocks[stock]['price']}")
    price_labels[stock].grid(row=0, column=1, padx=10)

    owned_labels[stock] = tk.Label(stock_frame, text=f"Owned: {stocks[stock]['owned']}")
    owned_labels[stock].grid(row=0, column=2, padx=10)

    quantity_entries[stock] = tk.Entry(stock_frame, width=5)
    quantity_entries[stock].insert(0, "1")
    quantity_entries[stock].grid(row=0, column=3)

    tk.Button(stock_frame, text="Buy", command=lambda s=stock: buy_stock(s)).grid(row=0, column=4)
    tk.Button(stock_frame, text="Sell", command=lambda s=stock: sell_stock(s)).grid(row=0, column=5)

update_button = tk.Button(root, text="Next Day (Update Prices)", command=update_prices)
update_button.pack(pady=10)

log_button = tk.Button(root, text="Show Transaction Log", command=show_transaction_log)
log_button.pack(pady=5)

portfolio_label = tk.Label(root, text="Total Portfolio Value: $0.00", font=("Helvetica", 12, "italic"))
portfolio_label.pack(pady=10)

status_label = tk.Label(root, text="", font=("Helvetica", 12, "bold"))
status_label.pack()

update_display()

root.mainloop()