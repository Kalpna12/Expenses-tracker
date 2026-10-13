# Expenses Tracker

A simple desktop-based expense management application built using **Python, Tkinter, and SQLite**. It helps users manage daily expenses, set a monthly budget, and track their spending and remaining budget through an easy-to-use graphical interface.

## Features

- **Add Expenses:** Record expense name, amount, and purchase date.
- **View Expenses:** Display saved expenses in a table with unique IDs.
- **Update Expenses:** Edit previously saved expense records.
- **Delete Expenses:** Remove unwanted expense records.
- **Monthly Budget:** Set or update your monthly budget.
- **Budget Summary:** View the monthly budget, total expenses for the current month, and remaining budget on the main screen.
- **Total Spending:** View the total expenses across all saved records.
- **Data Persistence:** Store expenses and budget information in an SQLite database.
- **Input Validation:** Validate expense names, positive amounts, and dates in `YYYY-MM-DD` format.
- **Automatic Database Creation:** Create the database and required tables when the application starts.

## Technologies Used

- **Python** — Application logic
- **Tkinter** — Graphical user interface
- **SQLite** — Database management
- **datetime** — Date validation and monthly expense calculations

## Project Structure

```text
Expenses-Tracker/
│
├── main.py
├── MyDatabase.py
├── expense_tracker.db
└── README.md
```

**Note:** `expense_tracker.db` is created automatically when you run the application for the first time. It does not need to be created manually.

## Requirements

- Python 3.8 or later recommended
- Tkinter (usually included with standard Python installations)
- SQLite (included with Python's `sqlite3` module)

No external Python packages are required.

## Installation and Setup

### 1. Install Python

Download and install Python from:

https://www.python.org/downloads/

On Windows, enable **Add Python to PATH** during installation.

### 2. Download or Clone the Project

If your project is hosted on GitHub, run:

```bash
git clone <your-repository-url>
cd Expenses-Tracker
```

Alternatively, download the project files and extract them into a folder.

### 3. Check the Project Files

Make sure these two Python files are in the same directory:

- `main.py`
- `MyDatabase.py`

The application uses `expense_tracker.db` as its database file.

### 4. Run the Application

Open a terminal in the project directory and execute:

```bash
python main.py
```

If your system uses the Python launcher on Windows, you can also run:

```bash
py main.py
```

The application window will open automatically.

## How to Use

### Set a Monthly Budget

1. Enter your desired budget in the budget field.
2. Click **Save Budget**.
3. The application saves the budget in SQLite and displays it on the screen.

You can update the budget whenever necessary.

### Add an Expense

1. Enter the expense name.
2. Enter the amount in rupees.
3. Enter the purchase date in `YYYY-MM-DD` format, or click **Today**.
4. Click **Save Expense**.

The saved expense appears in the table, and the budget summary updates automatically.

### Update an Expense

1. Select an expense from the table.
2. Modify its name, amount, or date.
3. Click **Update Selected**.

The updated record is saved in the database.

### Delete an Expense

1. Select an expense from the table.
2. Click **Delete Selected**.
3. Confirm the deletion.

The record is removed from the database, and the totals are recalculated.

### View Expense Summaries

The main screen displays:

- **Budget:** The saved monthly budget.
- **Expenses This Month:** Expenses dated within the current calendar month.
- **Remaining Budget:** Monthly budget minus expenses for the current month.
- **All-time Expenses:** Total spending across all saved records.

The **Monthly Summary** and **Total Spent** buttons also display detailed summaries.

## Database Design

The application uses SQLite with two tables.

### 1. `expense_record`

Stores individual expense records.

| Column | Description |
|---|---|
| `ID` | Unique auto-incrementing expense ID |
| `item_name` | Name of the expense |
| `item_price` | Expense amount; must be greater than zero |
| `purchase_date` | Purchase date in ISO format (`YYYY-MM-DD`) |

### 2. `budget`

Stores the monthly budget.

| Column | Description |
|---|---|
| `ID` | Fixed identifier (`1`) for the budget |
| `amount` | Saved budget amount, greater than zero |

The budget is updated in place, so only one current budget amount is stored.

## Budget Calculation

The application calculates the remaining budget using:

```text
Remaining Budget = Monthly Budget - Expenses This Month
```

For example, if the monthly budget is ₹5,000 and monthly expenses total ₹1,250:

```text
Monthly Budget:   ₹5,000.00
Expenses:         ₹1,250.00
Remaining Budget: ₹3,750.00
```

Expenses are grouped by their purchase date, not by when they were entered into the application. The all-time total includes expenses from every month.

## Data Storage and Persistence

- Expense records and budget information are saved in `expense_tracker.db`.
- Saved data remains available after closing and reopening the application.
- The application automatically creates the database and tables if they do not exist.

**Important:** Run `main.py` from the project directory so that the database file is created and accessed in the expected location.

## Error Handling and Validation

The application checks for common input errors, including:

- Empty expense names
- Invalid or non-positive expense amounts
- Invalid purchase dates
- Invalid or non-positive budgets
- Attempts to update or delete without selecting a record

Database errors are reported through dialog boxes.

## Future Improvements

Possible enhancements include:

- Expense categories, such as food, travel, shopping, and bills
- Monthly and yearly reports
- Charts showing spending patterns
- Exporting expense records to CSV or Excel
- Searching and filtering expenses
- Separate budgets for each month
- Automatic warnings when spending exceeds the budget
- Improved interface styling and dark mode

## Contributing

Suggestions and improvements are welcome. To contribute:

1. Fork the repository.
2. Create a new branch for your changes.
3. Make and test your changes.
4. Submit a pull request.

## License

This project is available for learning and personal use. Add a suitable open-source license, such as the MIT License, if you intend to distribute it publicly.

---

**Developed with Python, Tkinter, and SQLite.**
