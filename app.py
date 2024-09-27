from flask import Flask, render_template, request
import pusher
import mysql.connector
import datetime
import pytz

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="185.232.14.52",
        database="u760464709_tst_sep",
        user="u760464709_tst_sep_usr",
        password="dJ0CIAFF="
    )

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")

@app.route("/alumnos/guardar", methods=["POST"])
def guardar():
    matricula = request.form.get("txtMatriculaFA")
    nombreapellido = request.form.get("txtNombreApellidoFA")
    return f"Matrícula {matricula} Nombre y Apellido {nombreapellido}"

@app.route("/buscar")
def buscar():
    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute(""SELECT * FROM sensor_log ORDER BY Id_Log DESC")
    registros = cursor.fetchall()
    cursor.close()
    con.close()
    return {"registros": registros}  # Devuelve como JSON

@app.route("/contenido")
def contenido():
     con = get_db_connection()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_usuarios")
    registros = cursor.fetchall()
    cursor.close()
    con.close()
    return {"registros": registros} 
    
    return render_template("contenido.html")

@app.route("/registrar", methods=["GET"])
def registrar():
    args = request.args

    if "temperatura" not in args or "humedad" not in args:
        return "Faltan parámetros", 400

    con = get_db_connection()
    cursor = con.cursor()

    sql = "INSERT INTO sensor_log (Temperatura, Humedad, Fecha_Hora) VALUES (%s, %s, %s)"
    val = (args["temperatura"], args["humedad"], datetime.datetime.now(pytz.timezone("America/Matamoros")))
    cursor.execute(sql, val)
    con.commit()
    cursor.close()
    con.close()

    pusher_client = pusher.Pusher(
        app_id="1766042",
        key="b4444a8caff165daf46a",
        secret="1442ec24356a6e4ac6ce",
        cluster="eu",
        ssl=True
    )
    
    pusher_client.trigger("canalRegistrosTemperaturaHumedad", "registroTemperaturaHumedad", args)
    return args

@app.route("/reg", methods=["GET"])
def reg():
    args = request.args
    return args  # Puedes agregar lógica adicional aquí

if __name__ == "__main__":
    app.run(debug=True)
