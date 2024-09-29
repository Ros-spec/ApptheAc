from flask import Flask, render_template, request, jsonify
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
    cursor.execute("SELECT * FROM tst0_usuarios ORDER BY Id_Usuarios DESC")
    registros = cursor.fetchall()
    cursor.close()
    con.close()
    return registros # Devuelve como JSON

# @app.route("/contenido")
# def contenido():
#         con = get_db_connection()  # Asegúrate de que esto funcione
#         cursor = con.cursor()  # Esto puede fallar si la conexión es None
#         cursor.execute("SELECT * FROM tst0_usuarios")
#         registros = cursor.fetchall()
#     return render_template("contenido.html")


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

@app.route("/datos")
def resdatos():
    return render_template("registro.html")


@app.route("/guardardatos", methods=["POST"])
def fun():
  def guardar_encuesta():
    try:
        # Verificar que la conexión esté activa
        if not con.is_connected():
            con.reconnect()

        # Obtener los datos del formulario
        id = request.form["txtid"]
        nombre = request.form["txtnombre"]
        contra = request.form["txtpass1"]

        cursor = con.cursor()

        # Inserción en la base de datos
        sql = "INSERT INTO tst0_usuarios (Id_Usuario, Nombre_Usuario, Contrasena) VALUES (%s, %s, %s)"
        val = (id, nombre, contra)
        cursor.execute(sql, val)
        con.commit()

        # Disparar el evento con Pusher para actualizar en tiempo real
        pusher_client = pusher.Pusher(
            app_id="1766042",
            key="b4444a8caff165daf46a",
            secret="1442ec24356a6e4ac6ce",
            cluster="eu",
            ssl=True
        )
        
        pusher_client.trigger("registro", "nuevo", {
            "ID": id,
            "nombre": nombre,
            "contraseña": contra
        })

        # Devolver una respuesta JSON de éxito
        return jsonify({"success": True, "message": "Encuesta guardada exitosamente!"})

    except mysql.connector.Error as err:
        print(f"Error al guardar la encuesta: {err}")
        return jsonify({"success": False, "message": f"Error al guardar la encuesta: {err}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
