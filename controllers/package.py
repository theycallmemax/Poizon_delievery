from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.package_model import get_package_thing
from models.cabinet_model import get_client

@app.route('/package', methods=['get'])
def package():
    conn = get_db_connection()
    package_id = request.args.get('return')
    print(package_id)

    # Другой код обработки запроса

    df_package_thing = get_package_thing(conn, package_id)
    df_client = get_client(conn)

    return render_template(
        'package.html',
        client_id=session['client_id'],
        package_id=package_id,
        package_thing = df_package_thing,
        combo_box = df_client,
        len=len
    )
