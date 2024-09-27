
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
    
    con.close()
    return registros

@app.route("/registrar", methods=["GET"])
def registrar():
  args = request.args
  
     if not con.is_connected():
         con.reconnect()

    cursor = con.cursor()

    sql = "INSERT INTO tst0_usuarios (Id_Usuario, Nombre_Usuario, Contrasena) VALUES (%s, %s, %s)"
    val = (9, args["txtname"], args["txtpass1"])  # Cambia "4" a 4 si es un entero.

     try:
         cursor.execute(sql, val)
         con.commit()  # Asegúrate de hacer commit si es necesario
     except Exception as e:
         print("Ocurrió un error:", e)
     finally:
         con.close()  # Asegúrate de cerrar la conexión
    

    # pusher_client = pusher.Pusher(
    #     app_id="1766042",
    #     key="b4444a8caff165daf46a",
    #     secret="1442ec24356a6e4ac6ce",
    #     cluster="eu",
    #     ssl=True
    # )

    # pusher_client.trigger("canal", "registrocontenido", args)
  return args
