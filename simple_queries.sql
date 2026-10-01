-- Напишите запросы, которые выводят следующую информацию:
-- 1. "имя контакта" и "город" (contact_name, city) из таблицы customers (только эти две колонки)
SELECT DISTINCT contact_name AS "имя_контакта", city AS "город" FROM customers;

-- 2. идентификатор заказа и разницу между датами формирования (order_date) заказа
-- и его отгрузкой (shipped_date) из таблицы orders
SELECT order_id, shipped_date - order_date AS "разница_в_днях" FROM orders;


-- 3. все города без повторов, в которых зарегистрированы заказчики (customers)
SELECT DISTINCT city FROM customers;


-- 4. количество заказов (таблица orders)
SELECT COUNT(*) AS "общее_количество_заказов" FROM orders;


-- 5. количество стран, в которые отгружался товар (таблица orders, колонка ship_country)
SELECT COUNT(DISTINCT ship_country) AS "количество_уникальных_стран" FROM orders;
