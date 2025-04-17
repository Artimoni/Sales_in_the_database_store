import sqlite3
from random import randint

def add_sample_items():
    products = [
        ('MacBook Pro', 'Ноутбуки', 1999.99, randint(5, 20)),
        ('iPhone 15', 'Телефоны', 999.99, randint(10, 30)),
        ('Чайник Bosch', 'Техника', 49.99, randint(15, 40)),
        ('Python для чайников', 'Книги', 29.99, randint(8, 25))
    ]
    
    with sqlite3.connect('store.db') as db:
        db.executemany('''
        INSERT INTO Items (title, type, cost, amount)
        VALUES (?, ?, ?, ?)
        ''', products)

if __name__ == '__main__':
    add_sample_items()
