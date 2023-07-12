import pandas

def get_adress(conn, client_id):
    return pandas.read_sql('''select  client_name as "ФИО:", phone as "Номер телефона:",  city_name as "Город:", Client.adress as "Адрес:",  c_index as "Индекс:",  Post_point.adress as "Адрес пункта выдачи:"
from Client
join package USING(client_id)
join Post_point on package.point_id = Post_point.post_point_id
join City using(city_id)
where client_id = :p_client
GROUP by Client.adress''', conn, params={"p_client": client_id})

def get_new_client(conn, new_name, new_phone, new_adress, new_index):
    cur = conn.cursor()
    cur.execute(
        '''INSERT INTO Client (client_name, phone, adress, c_index)
        SELECT :p_new_name, :p_new_phone, :p_new_adress, :p_new_index
        WHERE NOT EXISTS (
            SELECT 1 FROM Client WHERE client_name = :p_new_name
        )''',
        {"p_new_name": new_name, "p_new_phone": new_phone, "p_new_adress": new_adress, "p_new_index": new_index}
    )

    conn.commit()
    return cur.lastrowid


def get_new_city(conn, new_city):
    cur = conn.cursor()
    cur.execute(
        '''INSERT INTO City (city_name)
        SELECT :p_new_city
        WHERE NOT EXISTS (
            SELECT 1 FROM City WHERE city_name = :p_new_city
        )''',
        {"p_new_city": new_city}
    )

    conn.commit()
    return cur.lastrowid


def get_new_point(conn, new_point):
    cur = conn.cursor()
    cur.execute(
        '''INSERT INTO Post_point (point_number, adress, company_id, city_id)
        SELECT "1", :p_new_point, "1", (SELECT city_id FROM City ORDER BY city_id DESC LIMIT 1)
        WHERE NOT EXISTS (
            SELECT 1 FROM Post_point WHERE adress = :p_new_point
        )''',
        {"p_new_point": new_point}
    )

    conn.commit()
    return cur.lastrowid


def get_new_package(conn):
    cur = conn.cursor()
    cur.execute('''insert into Package (client_id, pay, point_id, tariff_id)
        select (SELECT client_id
        FROM Client
        ORDER BY client_id DESC
        LIMIT 1) as client_id, 0, (SELECT post_point_id
        FROM Post_point
        ORDER BY post_point_id DESC
        LIMIT 1) as point_id, 1''')
    conn.commit()
    return cur.lastrowid


def get_new_thing(conn, new_ref):
    cur = conn.cursor()
    cur.execute(
        '''INSERT INTO Thing (package_id, ref)
        SELECT (SELECT package_id FROM Package ORDER BY package_id DESC LIMIT 1) as package_id, :p_new_ref''',
        {"p_new_ref": new_ref}
    )

    conn.commit()
    return cur.lastrowid

def get_package_old(conn, client_id):
    cur = conn.cursor()
    cur.execute(
        '''INSERT INTO Package (client_id, pay, point_id, tariff_id)
        SELECT :p_client, 0, (select post_point_id 
                                from Post_point 
                                JOIN Package on  Post_point.post_point_id = Package.point_id
                                JOIN Client USING (client_id) 
                                where Client.client_id = :p_client 
                                Group by post_point_id
                                Order by post_point_id desc
                                limit 1), 1''', {"p_client": client_id}
    )

    conn.commit()
    return cur.lastrowid

def get_new_status(conn):
    cur = conn.cursor()
    cur.execute(
        ''' insert into Package_status (package_id, status_id, status_date)
            select (SELECT package_id FROM Package ORDER BY package_id DESC LIMIT 1), 1, date('now')'''
    )

    conn.commit()
    return cur.lastrowid

