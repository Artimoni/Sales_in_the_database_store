import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class StoreManager:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.load_items()
        
    def setup_ui(self):
        self.root.title("Store Manager Pro")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        self.root.configure(bg='white')
        
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('.', background='white', foreground='black', font=('Segoe UI', 10))
        style.configure('TButton', padding=6)
        style.configure('Treeview', rowheight=25)
        style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'))
        
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        ttk.Label(header_frame, text="Store Manager Pro", 
                 font=('Segoe UI', 16, 'bold')).pack()
        
        nav_frame = ttk.Frame(main_container)
        nav_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.items_btn = ttk.Button(nav_frame, text="Товары", command=self.show_items)
        self.items_btn.pack(side=tk.LEFT, padx=5)
        
        self.sales_btn = ttk.Button(nav_frame, text="Продажи", command=self.show_sales)
        self.sales_btn.pack(side=tk.LEFT, padx=5)
        
        self.main_area = ttk.Frame(main_container)
        self.main_area.pack(fill=tk.BOTH, expand=True)
        
        self.status_bar = ttk.Label(main_container, text="Готово", relief=tk.SUNKEN, 
                                   anchor=tk.W, padding=5)
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
    
    def load_items(self):
        try:
            with sqlite3.connect('store.db') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT item_id, title, cost, amount FROM Items ORDER BY title")
                self.items = cursor.fetchall()
            self.status_bar.config(text="Товары успешно загружены")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить товары: {str(e)}")
            self.status_bar.config(text="Ошибка загрузки товаров")
    
    def show_items(self):
        self.clear_main_area()
        
        tree_frame = ttk.Frame(self.main_area)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scroll_y = ttk.Scrollbar(tree_frame)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree = ttk.Treeview(tree_frame, columns=("ID", "Название", "Цена", "Количество"), 
                           show="headings", yscrollcommand=scroll_y.set)
        tree.pack(fill=tk.BOTH, expand=True)
        
        scroll_y.config(command=tree.yview)
        
        tree.column("ID", width=50, anchor=tk.CENTER)
        tree.column("Название", width=300)
        tree.column("Цена", width=100, anchor=tk.E)
        tree.column("Количество", width=100, anchor=tk.CENTER)
        
        tree.heading("ID", text="ID")
        tree.heading("Название", text="Название")
        tree.heading("Цена", text="Цена")
        tree.heading("Количество", text="Количество")
        
        for item in self.items:
            try:
                price = float(item[2])
                values = (item[0], item[1], f"{price:.2f}", item[3])
            except ValueError:
                values = (item[0], item[1], item[2], item[3])
                
            if item[3] <= 0:
                tree.insert("", tk.END, values=values, tags=('out_of_stock',))
            else:
                tree.insert("", tk.END, values=values)
        
        tree.tag_configure('out_of_stock', foreground='gray')
        
        btn_frame = ttk.Frame(self.main_area)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(btn_frame, text="Новая продажа", command=self.add_sale).pack()
    
    def add_sale(self):
        self.sale_window = tk.Toplevel(self.root)
        self.sale_window.title("Оформление продажи")
        self.sale_window.geometry("500x400")
        
        main_frame = ttk.Frame(self.sale_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(main_frame, text="Выберите товары для продажи", 
                 font=('Segoe UI', 11, 'bold')).pack(pady=(0, 10))
        
        canvas = tk.Canvas(main_frame, borderwidth=0, highlightthickness=0, bg='white')
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        header_frame = ttk.Frame(scrollable_frame)
        header_frame.pack(fill=tk.X)
        
        ttk.Label(header_frame, text="Товар", font=('Segoe UI', 9, 'bold')).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(header_frame, text="Доступно", font=('Segoe UI', 9, 'bold')).grid(row=0, column=1)
        ttk.Label(header_frame, text="Кол-во", font=('Segoe UI', 9, 'bold')).grid(row=0, column=2)
        
        self.sale_vars = []
        for item in self.items:
            item_frame = ttk.Frame(scrollable_frame)
            item_frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(item_frame, text=item[1]).grid(row=0, column=0, sticky=tk.W)
            ttk.Label(item_frame, text=str(item[3])).grid(row=0, column=1)
            
            var = tk.IntVar(value=0)
            spin = ttk.Spinbox(item_frame, from_=0, to=item[3], textvariable=var, width=5)
            spin.grid(row=0, column=2)
            
            if item[3] <= 0:
                spin.config(state='disabled')
            
            self.sale_vars.append((item[0], var, item[3]))
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(btn_frame, text="Отмена", command=self.sale_window.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Оформить", command=self.process_sale).pack(side=tk.RIGHT)
    
    def process_sale(self):
        selected = []
        errors = []
        
        for item_id, var, available in self.sale_vars:
            qty = var.get()
            if qty > 0:
                if qty > available:
                    errors.append(f"Превышено доступное количество для товара ID {item_id} (макс: {available})")
                else:
                    selected.append((item_id, qty))
        
        if errors:
            messagebox.showerror("Ошибка", "\n".join(errors), parent=self.sale_window)
            return
            
        if not selected:
            messagebox.showerror("Ошибка", "Не выбрано ни одного товара", parent=self.sale_window)
            return
            
        try:
            with sqlite3.connect('store.db') as conn:
                cursor = conn.cursor()
                
                cursor.execute("INSERT INTO Transactions (trans_time, sum) VALUES (?, 0)", 
                             (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),))
                trans_id = cursor.lastrowid
                
                total = 0
                for item_id, qty in selected:
                    cursor.execute("SELECT cost FROM Items WHERE item_id = ?", (item_id,))
                    cost = float(cursor.fetchone()[0])
                    item_total = cost * qty
                    total += item_total
                    
                    cursor.execute('''
                    INSERT INTO TransactionItems (trans_id, item_id, qty, item_cost)
                    VALUES (?, ?, ?, ?)
                    ''', (trans_id, item_id, qty, cost))
                    
                    cursor.execute("UPDATE Items SET amount = amount - ? WHERE item_id = ?", 
                                 (qty, item_id))
                
                cursor.execute("UPDATE Transactions SET sum = ? WHERE trans_id = ?", 
                             (total, trans_id))
                conn.commit()
                
            messagebox.showinfo("Успех", f"Продажа оформлена. Сумма: {total:.2f}", parent=self.sale_window)
            self.sale_window.destroy()
            self.load_items()
            self.status_bar.config(text=f"Продажа оформлена. Сумма: {total:.2f}")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при оформлении продажи: {str(e)}", parent=self.sale_window)
            self.status_bar.config(text="Ошибка при оформлении продажи")

    def show_sales(self):
        self.clear_main_area()
        
        filter_frame = ttk.Frame(self.main_area)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(filter_frame, text="Дата продажи:").pack(side=tk.LEFT)
        
        self.date_entry = ttk.Entry(filter_frame)
        self.date_entry.pack(side=tk.LEFT, padx=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        ttk.Button(filter_frame, text="Показать", command=self.load_sales).pack(side=tk.LEFT)
        
        tree_frame = ttk.Frame(self.main_area)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scroll_y = ttk.Scrollbar(tree_frame)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.sales_tree = ttk.Treeview(tree_frame, columns=("ID", "Время", "Сумма"), 
                                     show="headings", yscrollcommand=scroll_y.set)
        self.sales_tree.pack(fill=tk.BOTH, expand=True)
        
        scroll_y.config(command=self.sales_tree.yview)
        
        self.sales_tree.column("ID", width=50, anchor=tk.CENTER)
        self.sales_tree.column("Время", width=150)
        self.sales_tree.column("Сумма", width=100, anchor=tk.E)
        
        self.sales_tree.heading("ID", text="ID")
        self.sales_tree.heading("Время", text="Время")
        self.sales_tree.heading("Сумма", text="Сумма")
        
        self.load_sales()
    
    def load_sales(self):
        date = self.date_entry.get()
        
        try:
            with sqlite3.connect('store.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''
                SELECT trans_id, trans_time, sum 
                FROM Transactions 
                WHERE date(trans_time) = ?
                ORDER BY trans_time DESC
                ''', (date,))
                
                self.sales_tree.delete(*self.sales_tree.get_children())
                
                total = 0
                for row in cursor.fetchall():
                    self.sales_tree.insert("", tk.END, values=(row[0], row[1], f"{float(row[2]):.2f}"))
                    total += float(row[2])
                
                if self.sales_tree.get_children():
                    self.sales_tree.insert("", tk.END, values=("", "ИТОГО:", f"{total:.2f}"))
                    self.sales_tree.tag_configure('total', background='#f0f0f0', font=('Segoe UI', 9, 'bold'))
                    self.sales_tree.item(self.sales_tree.get_children()[-1], tags=('total',))
            
            self.status_bar.config(text=f"Продажи за {date} загружены. Итого: {total:.2f}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить продажи: {str(e)}")
            self.status_bar.config(text="Ошибка загрузки продаж")
    
    def clear_main_area(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = StoreManager(root)
    root.mainloop()
