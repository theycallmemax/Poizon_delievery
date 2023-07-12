from flask import Flask
app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# здесь должны импортироваться все программы-контроллеры, # размещенные в папке controllers
import controllers.index
import controllers.cabinet
import controllers.zakaz
import controllers.package