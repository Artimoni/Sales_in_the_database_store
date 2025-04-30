import sqlite3
from random import randint
from datetime import datetime, timedelta
from tkinter import messagebox

def add_sample_items():
    products = [
        ('MacBook Pro', 'Ноутбуки', 1999.99, randint(5, 20)),
        ('iPhone 15', 'Телефоны', 999.99, randint(10, 30)),
        ('Чайник Bosch', 'Техника', 49.99, randint(15, 40)),
        ('Python для чайников', 'Книги', 29.99, randint(8, 25))
    ]
    
    try:
        with sqlite3.connect('store.db') as db:
            db.executemany('''
            INSERT INTO Items (title, type, cost, amount)
            VALUES (?, ?, ?, ?)
            ''', products)
        print("Тестовые товары успешно добавлены")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось добавить товары: {str(e)}")

def add_sample_sales():
    try:
        with sqlite3.connect('store.db') as db:
            cursor = db.cursor()
            items = cursor.execute("SELECT item_id, cost FROM Items").fetchall()
            
            for _ in range(10):
                trans_time = (datetime.now() - timedelta(days=randint(0, 30))).strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("INSERT INTO Transactions (trans_time, sum) VALUES (?, 0)", (trans_time,))
                trans_id = cursor.lastrowid
                
                total = 0
                for _ in range(randint(1, 3)):
                    item_id, cost = items[randint(0, len(items)-1)]
                    qty = randint(1, 3)
                    total += cost * qty
                    
                    cursor.execute('''
                    INSERT INTO TransactionItems (trans_id, item_id, qty, item_cost)
                    VALUES (?, ?, ?, ?)
                    ''', (trans_id, item_id, qty, cost))
                    
                cursor.execute("UPDATE Transactions SET sum = ? WHERE trans_id = ?", (total, trans_id))
                db.commit()
        print("Тестовые продажи успешно добавлены")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось добавить продажи: {str(e)}")

if __name__ == '__main__':
    print("Добавление тестовых данных")
    add_sample_items()
    add_sample_sales()
    print("Готово!")
