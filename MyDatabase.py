import sqlite3


class Database:
    def __init__(self, db="expense_tracker.db"):
        self.conn = sqlite3.connect(db)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cur = self.conn.cursor()
        self.createTables()

    def createTables(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS expense_record (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                item_price REAL NOT NULL CHECK (item_price > 0),
                purchase_date TEXT NOT NULL
            )
        """)

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS budget (
                ID INTEGER PRIMARY KEY CHECK (ID = 1),
                amount REAL NOT NULL CHECK (amount > 0)
            )
        """)

        self.conn.commit()

    def setBudget(self, amount):
        amount = float(amount)

        if amount <= 0:
            raise ValueError("Budget must be greater than zero.")

        self.cur.execute("""
            INSERT INTO budget (ID, amount)
            VALUES (1, ?)
            ON CONFLICT(ID)
            DO UPDATE SET amount = excluded.amount
        """, (amount,))

        self.conn.commit()

    def getBudget(self):
        result = self.cur.execute("""
            SELECT amount
            FROM budget
            WHERE ID = 1
        """).fetchone()

        return float(result[0]) if result else 0.0

    def fetchRecord(self):
        return self.cur.execute("""
            SELECT ID, item_name, item_price, purchase_date
            FROM expense_record
            ORDER BY purchase_date DESC, ID DESC
        """).fetchall()

    def insertRecord(self, item_name, item_price, purchase_date):
        with self.conn:
            self.conn.execute("""
                INSERT INTO expense_record
                    (item_name, item_price, purchase_date)
                VALUES (?, ?, ?)
            """, (item_name, float(item_price), purchase_date))

    def updateRecord(
        self, item_name, item_price, purchase_date, record_id
    ):
        with self.conn:
            self.conn.execute("""
                UPDATE expense_record
                SET item_name = ?,
                    item_price = ?,
                    purchase_date = ?
                WHERE ID = ?
            """, (
                item_name,
                float(item_price),
                purchase_date,
                int(record_id)
            ))

    def removeRecord(self, record_id):
        with self.conn:
            self.conn.execute("""
                DELETE FROM expense_record
                WHERE ID = ?
            """, (int(record_id),))

    def totalExpenses(self):
        result = self.cur.execute("""
            SELECT COALESCE(SUM(item_price), 0)
            FROM expense_record
        """).fetchone()

        return float(result[0])

    def monthlyExpenses(self, year_month):
        result = self.cur.execute("""
            SELECT COALESCE(SUM(item_price), 0)
            FROM expense_record
            WHERE substr(purchase_date, 1, 7) = ?
        """, (year_month,)).fetchone()

        return float(result[0])

    def close(self):
        self.conn.close()
