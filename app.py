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
  
@app.route("/contenido")
def contenido():
  con.close()
  return render_template("contenido.html")

@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_usuarios")

    registros = cursor.fetchall()

    return registros

@app.route("/registrar", methods=["POST"])
def registrar():
  # Nombre = request.form["txtname"]
  # Pass = request.form["txtpass1"]
  
pusher_client= pusher.Pusher(
      app_id = "1766042",
      key = "b4444a8caff165daf46a",
      secret = "1442ec24356a6e4ac6ce",
      cluster = "eu",
      ssl=True
    )
  
    sql = "INSERT INTO tst0_usuarios(Id_Usuario, Nombre_Usuario, Contrasena) VALUES(%s, %s, %s)"
    val = ["4", "ros","MMM"]
    cursor.execute(sql, val)
    
    con.commit()
    con.close()
  
    pusher_client.trigger("canal", "registrocontenido")
