import sqlite3

def init_db():
    with sqlite3.connect('store.db') as db:
        cursor = db.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            type TEXT NOT NULL,
            cost REAL NOT NULL,
            amount INTEGER NOT NULL
        )''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Transactions (
            trans_id INTEGER PRIMARY KEY AUTOINCREMENT,
            trans_time TEXT NOT NULL,
            sum REAL NOT NULL
        )''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS TransactionItems (
            trans_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            trans_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            qty INTEGER NOT NULL,
            item_cost REAL NOT NULL,
            FOREIGN KEY(trans_id) REFERENCES Transactions(trans_id),
            FOREIGN KEY(item_id) REFERENCES Items(item_id)
        )''')

if __name__ == '__main__':
    init_db()
