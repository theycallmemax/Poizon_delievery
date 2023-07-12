import pandas

def get_client(conn):

    return pandas.read_sql('''select * from Client''', conn)

def get_client_package(conn, client_id, pay_id, status_id, price_sort):
    search_str = "WHERE 1 = 1"

    if pay_id != 2:
        search_str += f" AND pay = {pay_id}"
    if status_id != 0:
        search_str += f" AND status_id = {status_id}"

    sort_str = ""
    if price_sort != "0" and price_sort != 0:
        sort_str += f" ORDER BY \"Стоимость в ₽\" {price_sort}"

    query = f'''
    WITH get_table (package_id, status_name, status_date, weight, total_cost, pay, button) AS (
        SELECT
            package_id,
            status_name,
            MAX(status_date),
            ROUND(SUM(weight), 2),
            ROUND(SUM(weight) * 600, 2),
            pay,
            button
        FROM
            Status
            JOIN package_status USING (status_id)
            JOIN package USING (package_id)
            JOIN Client USING (client_id)
            JOIN Thing USING (package_id)
            JOIN Tariff USING (tariff_id)
        WHERE client_id = ?
        GROUP BY package_id
    )
    SELECT
        package_id AS "Номер посылки",
        status_name AS Статус,
        MAX(status_date) AS "Дата статуса",
        weight AS "Вес в кг",
        total_cost AS "Стоимость в ₽",
        CASE WHEN pay = 1 THEN "Оплачено" ELSE "Не оплачено" END AS Оплата,
        button AS Посмотреть
    FROM
        get_table
    JOIN
        Status USING (status_name)
    {search_str}
    GROUP BY
        package_id
    {sort_str}
    '''

    return pandas.read_sql(query, conn, params=[client_id])


def get_status(conn):
    return pandas.read_sql('''SELECT distinct status_id, status_name 
                                FROM package  
                                JOIN package_status USING (package_id) 
                                join  Status USING(status_id)''', conn)