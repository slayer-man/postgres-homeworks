import csv
import psycopg


def fill_table_from_csv(table_name, file_name):
    with psycopg.connect(
            dbname="north",
            user="postgres",
            password="DeadMan32",
            port="5432",
            host="localhost"
    ) as conn:
        with conn.cursor() as cursor:
            with open(file_name) as csv_file:
                csv_reader = csv.reader(csv_file)
                header = next(csv_reader)

                if table_name == 'employees':
                    header.insert(0, 'employee_id')

                emp_id_counter = 1

                for row in csv_reader:
                    processed_row = [None if val.strip() == "" else val.strip() for val in row]

                    if table_name == 'employees':
                        processed_row.insert(0, str(emp_id_counter))
                        emp_id_counter += 1

                    placeholders = ", ".join(["%s"] * len(processed_row))
                    columns = ", ".join(header)
                    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

                    # Защита от дубликатов (пропуск ошибок уникальности)
                    if table_name == 'customers':
                        query += " ON CONFLICT (customer_id) DO NOTHING;"
                    elif table_name == 'employees':
                        query += " ON CONFLICT (employee_id) DO NOTHING;"
                    elif table_name == 'orders':
                        query += " ON CONFLICT (order_id) DO NOTHING;"
                    else:
                        query += ";"

                    cursor.execute(query, processed_row)

            print(f"Данные в таблицу {table_name} успешно импортированы.")


def main():
    fill_table_from_csv('customers', 'north_data/customers_data.csv')
    fill_table_from_csv('employees', 'north_data/employees_data.csv')
    fill_table_from_csv('orders', 'north_data/orders_data.csv')


if __name__ == "__main__":
    main()
