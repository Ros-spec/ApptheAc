from flask import Flask

from flask import render_template
from flask import request

import pusher

import mysql.connector
import datetime
import pytz

con = mysql.connector.connect(
  host="185.232.14.52",
  database="u760464709_tst_sep",
  user="u760464709_tst_sep_usr",
  password="dJ0CIAFF="
)

app = Flask(__name__)

@app.route("/")
def usuarios():
  return render_template("registro.html")

@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM sensor_log")

    registros = cursor.fetchall()

    return registros

@app.route("/registrar", methods=["GET"])
def registrar():
    pusher_client = pusher.Pusher(
      app_id = "1766042",
key = "b2cda443b1b3457d666e",
secret = "4a6a830012d1f16d0619",
cluster = "eu",
        ssl=True
    )

    pusher_client.trigger("canalRegistrosTemperaturaHumedad", "registroTemperaturaHumedad", request.args)
