import tkinter as tk
from tkinter import ttk
import sqlite3

# Создаем и подключаемся к базе данных
conn = sqlite3.connect('employees.db')
cursor = conn.cursor()

# Создаем таблицу для хранения сотрудников
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        full_name TEXT,
        phone_number TEXT,
        email TEXT,
        salary REAL
    )
''')
conn.commit()

# Функция для добавления нового сотрудника
def add_employee():
    full_name = full_name_entry.get()
    phone_number = phone_number_entry.get()
    email = email_entry.get()
    salary = float(salary_entry.get())

    cursor.execute('INSERT INTO employees (full_name, phone_number, email, salary) VALUES (?, ?, ?, ?)',
                   (full_name, phone_number, email, salary))
    conn.commit()

    update_treeview()

# Функция для обновления выбранного сотрудника
def update_employee():
    selected_item = tree.focus()
    if selected_item:
        new_full_name = full_name_entry.get()
        new_phone_number = phone_number_entry.get()
        new_email = email_entry.get()
        new_salary = float(salary_entry.get())
        employee_id = tree.item(selected_item, 'text')

        cursor.execute('''
            UPDATE employees
            SET full_name=?, phone_number=?, email=?, salary=?
            WHERE id=?
        ''', (new_full_name, new_phone_number, new_email, new_salary, employee_id))
        conn.commit()

        update_treeview()

# Функция для удаления выбранного сотрудника
def delete_employee():
    selected_item = tree.focus()
    if selected_item:
        employee_id = tree.item(selected_item, 'text')
        cursor.execute('DELETE FROM employees WHERE id=?', (employee_id,))
        conn.commit()

        update_treeview()

# Функция для поиска сотрудников по ФИО
def search_employee():
    search_query = search_entry.get()
    cursor.execute('SELECT * FROM employees WHERE full_name LIKE ?', ('%' + search_query + '%',))
    employees = cursor.fetchall()
    update_treeview(employees)

# Функция для очистки полей ввода
def clear_input_fields():
    full_name_entry.delete(0, tk.END)
    phone_number_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    salary_entry.delete(0, tk.END)

# Функция для обновления записей в Treeview
def update_treeview(employees=None):
    for row in tree.get_children():
        tree.delete(row)

    if employees is None:
        cursor.execute('SELECT * FROM employees')
        employees = cursor.fetchall()

    for employee in employees:
        tree.insert('', 'end', text=employee[0], values=(employee[1], employee[2], employee[3], employee[4]))

# Создаем главное окно
root = tk.Tk()
root.title("Список сотрудников компании")

# Фрейм для ввода данных
input_frame = ttk.LabelFrame(root, text="Информация о сотруднике")
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

full_name_label = ttk.Label(input_frame, text="ФИО:")
full_name_label.grid(row=0, column=0, padx=5, pady=5)
full_name_entry = ttk.Entry(input_frame)
full_name_entry.grid(row=0, column=1, padx=5, pady=5)

phone_number_label = ttk.Label(input_frame, text="Номер телефона:")
phone_number_label.grid(row=1, column=0, padx=5, pady=5)
phone_number_entry = ttk.Entry(input_frame)
phone_number_entry.grid(row=1, column=1, padx=5, pady=5)

email_label = ttk.Label(input_frame, text="Адрес электронной почты:")
email_label.grid(row=2, column=0, padx=5, pady=5)
email_entry = ttk.Entry(input_frame)
email_entry.grid(row=2, column=1, padx=5, pady=5)

salary_label = ttk.Label(input_frame, text="Заработная плата:")
salary_label.grid(row=3, column=0, padx=5, pady=5)
salary_entry = ttk.Entry(input_frame)
salary_entry.grid(row=3, column=1, padx=5, pady=5)

add_button = ttk.Button(input_frame, text="Добавить сотрудника", command=add_employee)
add_button.grid(row=4, columnspan=2, padx=5, pady=10)

update_button = ttk.Button(input_frame, text="Обновить сотрудника", command=update_employee)
update_button.grid(row=5, columnspan=2, padx=5, pady=10)

delete_button = ttk.Button(input_frame, text="Удалить сотрудника", command=delete_employee)
delete_button.grid(row=6, columnspan=2, padx=5, pady=10)

# Фрейм для поиска
search_frame = ttk.LabelFrame(root, text="Поиск")
search_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

search_label = ttk.Label(search_frame, text="Поиск по ФИО:")
search_label.grid(row=0, column=0, padx=5, pady=5)
search_entry = ttk.Entry(search_frame)
search_entry.grid(row=0, column=1, padx=5, pady=5)

search_button = ttk.Button(search_frame, text="Поиск", command=search_employee)
search_button.grid(row=1, columnspan=2, padx=5, pady=10)

clear_button = ttk.Button(search_frame, text="Очистить поля ввода", command=clear_input_fields)
clear_button.grid(row=2, columnspan=2, padx=5, pady=10)

# Создаем Treeview для отображения данных
tree = ttk.Treeview(root, columns=("ID", "ФИО", "Номер телефона", "Email", "Заработная плата"))
tree.heading("#1", text="ID")
tree.heading("#2", text="ФИО")
tree.heading("#3", text="Номер телефона")
tree.heading("#4", text="Email")
tree.heading("#5", text="Заработная плата")
tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Привязываем Treeview к вертикальной и горизонтальной прокрутке
vsb = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
vsb.grid(row=1, column=2, sticky="ns")
tree.configure(yscrollcommand=vsb.set)

hsb = ttk.Scrollbar(root, orient="horizontal", command=tree.xview)
hsb.grid(row=2, column=0, columnspan=2, sticky="ew")
tree.configure(xscrollcommand=hsb.set)

# Обновляем Treeview
update_treeview()

root.mainloop()

# Закрываем соединение с базой данных при выходе из программы
conn.close()
