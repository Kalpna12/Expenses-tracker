import tkinter as tk
from tkinter import ttk, messagebox
import datetime as dt
from MyDatabase import Database


# -------------------- MAIN WINDOW --------------------

ws = tk.Tk()
ws.title("Daily Expenses Tracker")
ws.geometry("950x700")
ws.minsize(800, 600)

data = Database(db="expense_tracker.db")

namevar = tk.StringVar(master=ws)
amtvar = tk.StringVar(master=ws)
dopvar = tk.StringVar(master=ws)
budget_var = tk.StringVar(master=ws)

budget_text = tk.StringVar(master=ws)
expense_text = tk.StringVar(master=ws)
remaining_text = tk.StringVar(master=ws)
all_time_text = tk.StringVar(master=ws)
month_text = tk.StringVar(master=ws)

selected_rowid = None
closing = False


# -------------------- HELPERS --------------------

def money(amount):
    return f"₹ {amount:,.2f}"


def clearEntries():
    global selected_rowid

    namevar.set("")
    amtvar.set("")
    dopvar.set(dt.date.today().isoformat())
    selected_rowid = None

    for item in tv.selection():
        tv.selection_remove(item)


def setDate():
    dopvar.set(dt.date.today().isoformat())


def getValidatedExpense():
    name = namevar.get().strip()
    amount_text = amtvar.get().strip()
    date_text = dopvar.get().strip()

    if not name:
        raise ValueError("Please enter an expense name.")

    try:
        amount = float(amount_text)
    except (ValueError, TypeError):
        raise ValueError("Enter a valid numeric amount.")

    if not (0 < amount < float("inf")):
        raise ValueError(
            "Amount must be greater than zero and finite."
        )

    try:
        purchase_date = dt.date.fromisoformat(date_text)
    except (ValueError, TypeError):
        raise ValueError(
            "Enter a valid date in YYYY-MM-DD format."
        )

    if purchase_date.isoformat() != date_text:
        raise ValueError(
            "Use the date format YYYY-MM-DD."
        )

    return name, amount, purchase_date.isoformat()


# -------------------- SUMMARY DISPLAY --------------------

summary = ttk.LabelFrame(
    ws, text="Monthly Budget Overview", padding=12
)
summary.pack(fill="x", padx=15, pady=(12, 5))

today = dt.date.today()
month_text.set(today.strftime("%B %Y"))

ttk.Label(
    summary, text="Budget",
    font=("Arial", 11, "bold")
).grid(row=0, column=0, padx=15, pady=4)

ttk.Label(
    summary, textvariable=budget_text,
    font=("Arial", 15, "bold")
).grid(row=1, column=0, padx=15, pady=4)

ttk.Label(
    summary, text="Expenses This Month",
    font=("Arial", 11, "bold")
).grid(row=0, column=1, padx=15, pady=4)

ttk.Label(
    summary, textvariable=expense_text,
    font=("Arial", 15, "bold")
).grid(row=1, column=1, padx=15, pady=4)

ttk.Label(
    summary, text="Remaining Budget",
    font=("Arial", 11, "bold")
).grid(row=0, column=2, padx=15, pady=4)

ttk.Label(
    summary, textvariable=remaining_text,
    font=("Arial", 15, "bold")
).grid(row=1, column=2, padx=15, pady=4)

ttk.Label(
    summary, textvariable=month_text
).grid(row=2, column=0, columnspan=3, pady=(5, 0))

ttk.Label(
    summary, textvariable=all_time_text
).grid(row=3, column=0, columnspan=3, pady=(3, 0))

for col in range(3):
    summary.columnconfigure(col, weight=1)


# -------------------- BUDGET INPUT --------------------

budget_frame = ttk.LabelFrame(
    ws, text="Set or Update Monthly Budget", padding=10
)
budget_frame.pack(fill="x", padx=15, pady=5)

ttk.Label(
    budget_frame, text="Budget Amount (₹):"
).pack(side="left", padx=5)

ttk.Entry(
    budget_frame, textvariable=budget_var, width=18
).pack(side="left", padx=5)

# Button is connected after set_budget is defined.


# -------------------- EXPENSE FORM --------------------

form = ttk.LabelFrame(
    ws, text="Expense Details", padding=10
)
form.pack(fill="x", padx=15, pady=5)

ttk.Label(form, text="Expense Name:").grid(
    row=0, column=0, sticky="w", padx=5, pady=5
)
ttk.Entry(form, textvariable=namevar).grid(
    row=0, column=1, sticky="ew", padx=5, pady=5
)

ttk.Label(form, text="Amount (₹):").grid(
    row=1, column=0, sticky="w", padx=5, pady=5
)
ttk.Entry(form, textvariable=amtvar).grid(
    row=1, column=1, sticky="ew", padx=5, pady=5
)

ttk.Label(form, text="Purchase Date:").grid(
    row=2, column=0, sticky="w", padx=5, pady=5
)
ttk.Entry(form, textvariable=dopvar).grid(
    row=2, column=1, sticky="ew", padx=5, pady=5
)

ttk.Button(
    form, text="Today", command=setDate
).grid(row=2, column=2, padx=5, pady=5)

form.columnconfigure(1, weight=1)


# -------------------- EXPENSE TABLE --------------------

table_frame = ttk.LabelFrame(
    ws, text="Saved Expenses", padding=8
)
table_frame.pack(fill="both", expand=True, padx=15, pady=8)

columns = ("ID", "name", "amount", "date")

tv = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=10
)

tv.heading("ID", text="ID")
tv.heading("name", text="Expense Name")
tv.heading("amount", text="Amount (₹)")
tv.heading("date", text="Purchase Date")

tv.column("ID", width=55, anchor="center")
tv.column("name", width=300)
tv.column("amount", width=150, anchor="e")
tv.column("date", width=160, anchor="center")

scrollbar = ttk.Scrollbar(
    table_frame, orient="vertical", command=tv.yview
)
tv.configure(yscrollcommand=scrollbar.set)

tv.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

tv.bind("<<TreeviewSelect>>", select_record_event := lambda event: select_record())


# -------------------- SUMMARY REFRESH --------------------

def updateSummary():
    current = dt.date.today()
    month_key = current.strftime("%Y-%m")

    budget = data.getBudget()
    monthly_total = data.monthlyExpenses(month_key)
    all_time_total = data.totalExpenses()
    remaining = budget - monthly_total

    budget_text.set(money(budget))
    expense_text.set(money(monthly_total))
    remaining_text.set(money(remaining))
    all_time_text.set(
        f"All-time expenses: {money(all_time_total)}"
    )
    month_text.set(
        f"Showing budget summary for {current.strftime('%B %Y')}"
    )


def refreshData():
    for item in tv.get_children():
        tv.delete(item)

    records = data.fetchRecord()

    for record in records:
        record_id, name, amount, purchase_date = record

        tv.insert(
            "",
            "end",
            iid=str(record_id),
            values=(
                record_id,
                name,
                f"{float(amount):,.2f}",
                purchase_date
            )
        )

    updateSummary()


# -------------------- BUDGET ACTION --------------------

def set_budget():
    text = budget_var.get().strip()

    try:
        amount = float(text)

        if not (0 < amount < float("inf")):
            raise ValueError

        data.setBudget(amount)
        budget_var.set("")
        updateSummary()

        messagebox.showinfo(
            "Budget Saved",
            f"Monthly budget set to {money(amount)}."
        )

    except ValueError:
        messagebox.showerror(
            "Invalid Budget",
            "Enter a valid budget greater than zero."
        )
    except Exception as error:
        messagebox.showerror("Database Error", str(error))


ttk.Button(
    budget_frame, text="Save Budget", command=set_budget
).pack(side="left", padx=5)


# -------------------- SAVE EXPENSE --------------------

def saveRecord():
    try:
        name, amount, purchase_date = getValidatedExpense()

        data.insertRecord(name, amount, purchase_date)

        refreshData()
        clearEntries()

        messagebox.showinfo(
            "Success", "Expense saved successfully."
        )

    except ValueError as error:
        messagebox.showerror("Validation Error", str(error))
    except Exception as error:
        messagebox.showerror("Database Error", str(error))


# -------------------- SELECT EXPENSE --------------------

def select_record():
    global selected_rowid

    selected = tv.selection()

    if not selected:
        return

    values = tv.item(selected[0], "values")

    if not values:
        return

    selected_rowid = int(values[0])
    namevar.set(values[1])
    amtvar.set(str(values[2]).replace(",", ""))
    dopvar.set(values[3])


# -------------------- UPDATE EXPENSE --------------------

def update_record():
    if selected_rowid is None:
        messagebox.showwarning(
            "Select Expense",
            "Select an expense from the table first."
        )
        return

    try:
        name, amount, purchase_date = getValidatedExpense()

        data.updateRecord(
            name, amount, purchase_date, selected_rowid
        )

        refreshData()
        clearEntries()

        messagebox.showinfo(
            "Success", "Expense updated successfully."
        )

    except ValueError as error:
        messagebox.showerror("Validation Error", str(error))
    except Exception as error:
        messagebox.showerror("Database Error", str(error))


# -------------------- DELETE EXPENSE --------------------

def deleteRow():
    global selected_rowid

    if selected_rowid is None:
        messagebox.showwarning(
            "Select Expense",
            "Select an expense from the table first."
        )
        return

    if not messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this expense?"
    ):
        return

    try:
        data.removeRecord(selected_rowid)

        refreshData()
        clearEntries()

        messagebox.showinfo(
            "Success", "Expense deleted successfully."
        )

    except Exception as error:
        messagebox.showerror("Database Error", str(error))


# -------------------- REPORT BUTTONS --------------------

def totalBalance():
    try:
        current = dt.date.today()
        budget = data.getBudget()
        total = data.monthlyExpenses(current.strftime("%Y-%m"))
        remaining = budget - total

        messagebox.showinfo(
            "Monthly Summary",
            f"Month: {current.strftime('%B %Y')}\n"
            f"Monthly Budget: {money(budget)}\n"
            f"Total Expense: {money(total)}\n"
            f"Budget Remaining: {money(remaining)}"
        )
    except Exception as error:
        messagebox.showerror("Error", str(error))


def totalSpent():
    try:
        total = data.totalExpenses()

        messagebox.showinfo(
            "Total Spent",
            f"All-time expenses: {money(total)}"
        )
    except Exception as error:
        messagebox.showerror("Error", str(error))


# -------------------- ACTION BUTTONS --------------------

buttons = ttk.Frame(ws, padding=(15, 0, 15, 10))
buttons.pack(fill="x")

ttk.Button(
    buttons, text="Save Expense", command=saveRecord
).pack(side="left", padx=4)

ttk.Button(
    buttons, text="Clear", command=clearEntries
).pack(side="left", padx=4)

ttk.Button(
    buttons, text="Update Selected", command=update_record
).pack(side="left", padx=4)

ttk.Button(
    buttons, text="Delete Selected", command=deleteRow
).pack(side="left", padx=4)

ttk.Button(
    buttons, text="Monthly Summary", command=totalBalance
).pack(side="left", padx=4)

ttk.Button(
    buttons, text="Total Spent", command=totalSpent
).pack(side="left", padx=4)

ttk.Button(
    buttons, text="Refresh", command=refreshData
).pack(side="left", padx=4)


# -------------------- CLOSE APPLICATION --------------------

def close_app():
    global closing

    if closing:
        return

    closing = True

    try:
        data.close()
    finally:
        ws.destroy()


# -------------------- START APPLICATION --------------------

try:
    dopvar.set(dt.date.today().isoformat())
    refreshData()
except Exception as error:
    messagebox.showerror(
        "Startup Error",
        f"Could not load the expense data:\n{error}"
    )

ws.protocol("WM_DELETE_WINDOW", close_app)
ws.mainloop()
