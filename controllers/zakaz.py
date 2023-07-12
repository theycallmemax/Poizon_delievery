from app import app
from flask import render_template, request, session, redirect, url_for
from utils import get_db_connection
from models.cabinet_model import get_client
from models.zakaz_model import get_adress, get_new_city, get_new_point, get_new_thing, get_new_package, get_new_client, get_package_old, get_new_status

@app.route('/zakaz', methods=['get'])
def zakaz():
    conn = get_db_connection()


    client_id = 1
    session['client_id'] = client_id
    sum = 0

    new_name = request.values.get('name')
    new_phone = request.values.get('phone')
    new_city = request.values.get('city')
    new_adress = request.values.get('adress')
    new_index = ('index')
    new_point = request.values.get('point')
    new_ref = request.values.getlist('ref')

    if request.values.get('new_adress') == 0:

        if new_name and new_phone and new_adress and new_index:
            # Создаем нового клиента
            session['client_id'] = get_new_client(conn, new_name, new_phone, new_adress, new_index)

        if new_city:
            # Создаем новый город
            get_new_city(conn, new_city)

        if new_point:
            # Создаем новый пункт выдачи
            get_new_point(conn, new_point)

        get_new_package(conn)
        get_new_status(conn)

        if new_ref:
            # Создаем новую вещь
            for i in new_ref:
                get_new_thing(conn, i)
    else:
        get_package_old(conn, client_id)
        get_new_status(conn)
        if new_ref:
            # Создаем новую вещь
            for i in new_ref:
                get_new_thing(conn, i)

    if request.values.get('cost'):
        cost = int(request.values.get('cost'))
        sum = cost * 12.7



    df_client = get_client(conn)
    df_adress = get_adress(conn, client_id)

    # Выводим форму
    html = render_template(
        'zakaz.html',
        client_id=session['client_id'],
        combo_box=df_client,
        combo_adress=df_adress,
        len=len,
        sum=sum
    )

    return html
