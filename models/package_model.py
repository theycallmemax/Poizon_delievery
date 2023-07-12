import pandas

def get_package_thing(conn, package_id):
    return pandas.read_sql('''select thing_name as Название, type_name as Тип, weight as Вес,  date_arrive as "Дата прибытия", ref as Ссылка
from Package
JOIN Thing USING (package_id)
JOIN thing_type on Thing.thing_type = thing_type.type_id
WHERE package_id = :p_package''', conn, params={"p_package": package_id})

