# 💰 Daily Expenses Tracker

A desktop-based expense management application built using **Python, Tkinter, and SQLite**. The application allows users to record daily expenses, manage transactions, and track spending against a customizable budget.

## 📌 Features

- **Add Expenses:** Record an expense name, amount, and purchase date.
- **View Expenses:** Display saved transactions in a table.
- **Update Expenses:** Edit existing expense records.
- **Delete Expenses:** Remove unwanted transactions.
- **Customizable Budget:** Set a budget according to your needs instead of using a fixed amount.
- **Expense Summary:** Calculate total expenses and view the remaining budget.
- **Date Selection:** Quickly enter the current date.
- **Persistent Storage:** Store expense records in an SQLite database.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Tkinter | Graphical user interface |
| SQLite | Local database storage |
| ttk.Treeview | Displaying expense records |
| datetime | Handling purchase dates |

## 📂 Project Structure

```text
Expenses-tracker/
│
├── main.py          # Main application and GUI
├── MyDatabase.py    # Database operations
├── test.db          # SQLite database
└── README.md        # Project documentation
```


## ⚙️ Installation and Setup

### 1. Install Python

Download and install Python 3 from [python.org](https://www.python.org/downloads/).

Tkinter and SQLite are included with most standard Python installations.

### 2. Clone the repository

```bash
git clone https://github.com/Kalpna12/Expenses-tracker.git
```

### 3. Navigate to the project directory

```bash
cd Expenses-tracker
```

### 4. Run the application

```bash
python main.py
```

The application window will open, allowing you to manage your expenses.

## 🚀 How to Use

1. Launch the application using `python main.py`.
2. Enter the expense name, amount, and purchase date.
3. Click **Save Record** to save a new expense.
4. Select a transaction from the table to edit or delete it.
5. Set your preferred budget using the budget input and **Set Budget** button.
6. Click **Total Balance** to view total spending and the remaining budget.
7. Use **Clear Entry** to reset the input fields.

## 🗄️ Database

The application uses SQLite to store expense records locally.

The `expense_record` table stores the following information:

| Field | Description |
|---|---|
| `item_name` | Name of the expense |
| `item_price` | Amount spent |
| `purchase_date` | Date of purchase |

A separate `budget` table can store the user's configurable budget.

## 🔮 Future Improvements

- Expense categories such as Food, Travel, Shopping, and Bills
- Monthly budgets and budget alerts
- Spending charts and graphical reports
- Search, filtering, and sorting transactions
- Export reports to CSV or Excel
- Income tracking and savings analysis
- Recurring expense management
- Improved input validation and user interface
- Database backup and restore

## 🎯 Project Objective

The objective of this project is to develop a simple and user-friendly desktop application for managing daily expenses while practicing Python programming, GUI development, SQL database operations, and CRUD functionality.

## 👨‍💻 Author

Kalpna Lovevanshi

