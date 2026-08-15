import sqlite3

def init_db():
    conn = sqlite3.connect("bills.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            amount REAL,
            due_date TEXT,
            recurring INTEGER DEFAULT 0,
            autopay INTEGER DEFAULT 0,
            paid INTEGER DEFAULT 0
        )
    """)

    cursor.execute("PRAGMA table_info(bills)")
    existing_columns = [row[1] for row in cursor.fetchall()]

    new_columns = {
            "recurring": "INTEGER DEFAULT 0",
            "autopay": "INTEGER DEFAULT 0",
            "paid": "INTEGER DEFAULT 0"
    }

    for col_name, col_type in new_columns.items():
        if col_name not in existing_columns:
            cursor.execute(f"ALTER TABLE bills ADD COLUMN {col_name} {col_type}")
#    try:
#        # Create recurring, autopay column and default it to 0
#        cursor.execute("ALTER TABLE bills ADD COLUMN recurring INTEGER DEFAULT 0")
#        cursor.execute("ALTER TABLE bills ADD COLUMN autopay INTEGER DEFAULT 0")
#    except sqlite3.OperationalError:
#        pass # column recurring already exists, ignore the error
    conn.commit()
    conn.close()


def add_bill(name, amount, due_date, recurring, autopay, paid):
    conn = sqlite3.connect("bills.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO bills (name, amount, due_date, recurring, autopay, paid) VALUES (?, ?, ?, ?, ?, ?)",
        (name, amount, str(due_date), recurring, autopay, paid)
    )
    conn.commit()
    conn.close()


def get_bills():
    conn = sqlite3.connect("bills.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bills ORDER BY due_date")
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_bill(bill_id):
    conn = sqlite3.connect("bills.db")
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM bills WHERE id = ?",
        (bill_id,)
    )
    conn.commit()
    conn.close()

def update_bill(bill_id, name, amount, due_date, recurring, autopay, paid):
    conn = sqlite3.connect("bills.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE bills SET name = ?, amount = ?, due_date = ?, recurring = ?, autopay = ?, paid = ? WHERE id = ?",
        (name, amount, str(due_date), recurring, autopay, paid, bill_id)
    )
    conn.commit()
    conn.close()


