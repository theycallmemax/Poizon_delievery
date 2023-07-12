from app import app
from flask import render_template, request
import constants
@app.route('/', methods=['GET'])
def index():
    city_id = 1
    lenth = 0
    width = 0
    height = 0
    weight = 0
    telegram = " "

        # получаем параметр из формы
    if request.values.get('lenth'):
        lenth = request.values.get('lenth')
        width = request.values.get('width')
        height = request.values.get('height')
        weight = request.values.get('weight')
        city_id = request.values.get('city')


    if request.values.get('default'):
        city_id = 1
        lenth = 0
        width = 0
        height = 0
        weight = 0

    city_select = request.values.get('city')
    if city_select is not None and city_select.isdigit():
        tarrif = constants.tariff_list[int(city_select)]
    else:
        # Обработка ситуации, когда city_select равно None или не является целым числом
        tarrif = 0
    summa = 0.1*float(lenth) + 0.1*float(height) + 0.1*float(width) + 600 * float(weight) * float(tarrif)

    if request.values.get('telegram-tag'):
        telegram = request.values.get('telegram-tag')
        print(telegram)

    html = render_template(
        'index.html',
        city_id = int(city_id),
        lenth=lenth,
        width =  width,
        height = height,
        weight = weight,
        summa=summa,
        city_list = constants.city,
        city_select = city_select,
        len=len,
        telegram=telegram
    )

    return html
