from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.cabinet_model import get_client, get_client_package, get_status


@app.route('/cabinet', methods=['get'])
def cabinet_view():

    conn = get_db_connection()

    client_id = 1
    session['client_id'] = client_id
    status_id = 0
    price_sort = 0
    pay_id = 2

    # нажата кнопка Найти
    if request.values.get('status'):
        status_id = int(request.values.get('status'))
    if request.values.get('price'):
        price_sort = request.values.get('price')
    if request.values.get('pay'):
        pay_id = int(request.values.get('pay'))



    # нажата кнопка сортировки по статусу
    df_client_package = get_client_package(conn, client_id, pay_id, status_id, price_sort)
    df_client = get_client(conn)
    df_status = get_status(conn)

    # выводим форму
    html = render_template(
        'cabinet.html',
        client_id=session['client_id'],
        client_package=df_client_package,
        combo_box=df_client,
        combo_status = df_status,
        status_id = status_id,
        len = len,
        price_sort = price_sort,
        pay_id = pay_id
    )
    return html
