# Импорт данных из CSV в PostgreSQL (База данных North)

Скрипт на Python для автоматического проектирования и наполнения реляционной базы данных `north` на основе CSV-файлов из директории `north_data`. 

Проект выполнен в рамках домашнего задания по работе с СУБД PostgreSQL и библиотекой `psycopg` (v3).

## Возможности скрипта
* **Автоматическая сборка SQL-запросов**: Универсальная функция самостоятельно читает заголовки из CSV и подставляет их в `INSERT`.
* **Защита от дубликатов**: Использование конструкции `ON CONFLICT DO NOTHING` позволяет безопасно запускать скрипт неограниченное количество раз.
* **Автогенерация ID**: Скрипт «на лету» нумерует сотрудников и добавляет `employee_id`, сохраняя исходный CSV-файл нетронутым.
* **Безопасность ресурсов**: Использование контекстных менеджеров `with` гарантирует автоматический `ROLLBACK` транзакции и закрытие соединений в случае любых ошибок.

## Подготовка базы данных

Перед запуском скрипта необходимо создать саму базу данных и таблицы.

1. Подключитесь к PostgreSQL через консоль:
   ```bash
   psql -U postgres
   ```
2. Создайте базу данных `north`:
   ```sql
   CREATE DATABASE north;
   ```
3. Через **Query Tool в pgAdmin** выполните SQL-код для создания таблиц и связей (содержимое файла `create_tables.sql`):
   ```sql
   CREATE TABLE employees (
       employee_id INT PRIMARY KEY,
       first_name VARCHAR(50) NOT NULL,
       last_name VARCHAR(50) NOT NULL,
       title VARCHAR(100),
       birth_date DATE,
       notes TEXT
   );

   CREATE TABLE customers (
       customer_id VARCHAR(10) PRIMARY KEY,
       company_name VARCHAR(100) NOT NULL,
       contact_name VARCHAR(100)
   );

   CREATE TABLE orders (
       order_id INT PRIMARY KEY,
       customer_id VARCHAR(10) REFERENCES customers(customer_id),
       employee_id INT REFERENCES employees(employee_id),
       order_date DATE,
       ship_city VARCHAR(50)
   );
   ```

## Запуск проекта

### 1. Требования
Для работы проекта необходим Python версии **3.10+** и установленная библиотека `psycopg`.

Установка зависимостей через Poetry (или pip):
```bash
poetry add psycopg
# или обычный pip:
pip install psycopg
```

### 2. Конфигурация
Откройте файл `main.py` и в функции `fill_table_from_csv` укажите ваш актуальный пароль от учетной записи `postgres`:
```python
password="Ваш_Пароль"
```

### 3. Запуск импорта
Убедитесь, что в корне проекта находится папка `north_data` с файлами `customers_data.csv`, `employees_data.csv` и `orders_data.csv`. Запустите скрипт:

```bash
python main.py
```

При успешном выполнении в консоли отобразится:
```text
Данные в таблицу customers успешно импортированы.
Данные в таблицу employees успешно импортированы.
Данные в таблицу orders успешно импортированы.

Process finished with exit code 0
```

##  Проверка данных
Чтобы убедиться, что связи между таблицами работают корректно, выполните тестовый запрос в pgAdmin:

```sql
SELECT 
    e.first_name || ' ' || e.last_name AS employee,
    COUNT(o.order_id) AS total_orders
FROM employees e
LEFT JOIN orders o ON e.employee_id = o.employee_id
GROUP BY e.employee_id, e.first_name, e.last_name
ORDER BY total_orders DESC;
```
