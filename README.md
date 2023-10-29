# Проект "Список сотрудников компании" на Python

Этот проект реализует приложение для управления списком сотрудников компании. Вот комментарии к ключевым частям кода:

## Создание и подключение к базе данных

```python
import sqlite3

# Создаем и подключаемся к базе данных
conn = sqlite3.connect('employees.db')
cursor = conn.cursor()

# Здесь мы используем библиотеку SQLite для создания и подключения к базе данных 'employees.db'.

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
```

Мы создаем таблицу "employees" для хранения информации о сотрудниках, включая их идентификатор, ФИО, номер телефона, адрес электронной почты и заработную плату.

## Функции для добавления, обновления и удаления сотрудников

```python
# Функция для добавления нового сотрудника
def delete_employee():
    selected_item = tree.focus()
    if selected_item:
        employee_id = tree.item(selected_item, 'text')
        cursor.execute('DELETE FROM employees WHERE id=?', (employee_id,))
        conn.commit()

        update_treeview()
```
Здесь мы создаем функции add_employee(), update_employee(), и delete_employee(), которые позволяют добавлять, 
обновлять и удалять сотрудников в базе данных.


## Функция для поиска сотрудников

```python
# Функция для поиска сотрудников по ФИО
def search_employee():
    search_query = search_entry.get()
    cursor.execute('SELECT * FROM employees WHERE full_name LIKE ?', ('%' + search_query + '%',))
    employees = cursor.fetchall()
    update_treeview(employees)
```
Эта функция search_employee() позволяет искать сотрудников по ФИО с использованием оператора LIKE в SQL.


## Функция для обновления Treeview

```python
# Функция для обновления записей в Treeview
def update_treeview(employees=None):
    for row in tree.get_children():
        tree.delete(row)

    if employees is None:
        cursor.execute('SELECT * FROM employees')
        employees = cursor.fetchall()

    for employee in employees:
        tree.insert('', 'end', text=employee[0], values=(employee[1], employee[2], employee[3], employee[4]))
```
Эта функция update_treeview() обновляет виджет Treeview, который используется для отображения данных о сотрудниках.


## Главное окно и интерфейс

```python
# Создаем главное окно
root = tk.Tk()
root.title("Список сотрудников компании")

# ...
```
Здесь мы создаем главное окно и интерфейс, включая поля ввода, кнопки и виджет Treeview для взаимодействия с пользователем.


## Закрытие соединения с базой данных

```python
# Закрываем соединение с базой данных при выходе из программы
conn.close()
```
По завершению работы приложения мы закрываем соединение с базой данных, чтобы предотвратить утечку ресурсов.

