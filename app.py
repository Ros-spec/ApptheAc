from flask import Flask, render_template, request, jsonify, make_response
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
    
@app.route("/buscar")
def buscar():
    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_usuarios")
    registros = cursor.fetchall()
    cursor.close()
    con.close()
    return registros 
    
@app.route("/")
def data():
    return render_template("registro.html")
     
def Eventopusher():
    pusher_client = pusher.Pusher(
        app_id="1766042",
        key="b4444a8caff165daf46a",
        secret="1442ec24356a6e4ac6ce",
        cluster="eu",
        ssl=True
    )

    id = request.form["txtid"]
    nombre = request.form["txtnombre"]
    contra = request.form["txtpass1"]

    pusher_client.trigger("registro", "nuevo", {
        "ID": id,
        "nombre": nombre,
        "contraseña": contra
    })

@app.route("/modificar", methods=["GET"])
def editar():
    con = get_db_connection()  # Abre la conexión aquí

    id = request.args["id"]

    cursor = con.cursor(dictionary=True)
    sql = """
    SELECT Id_Usuario, Nombre_Usuario, contrasena FROM tst0_usuarios
    WHERE Id_Usuario = %s
    """
    val = (id,)

    cursor.execute(sql, val)
    registros = cursor.fetchall()
    cursor.close()
    con.close()

    return make_response(jsonify(registros))

@app.route("/eliminar", methods=["GET"])
def eliminar():
    con = get_db_connection()  # Abre la conexión aquí

    id = request.args["id"]
    
    cursor = con.cursor(dictionary=True)
    sql = """
    DELETE FROM tst0_usuarios
    WHERE Id_Usuario = %s
    """
    val = (id,)

    cursor.execute(sql, val)
    con.commit()
    cursor.close()  # Asegúrate de cerrar el cursor
    con.close()     # Y también la conexión

    Eventopusher()

    return make_response(jsonify({}))

@app.route("/guardardatos", methods=["POST"])  # Asegúrate de que sea POST
def guardardatos():
    try:
        con = get_db_connection()  # Abre la conexión aquí
        # Obtener los datos del formulario
        id = request.form["txtid"]
        nombre = request.form["txtnombre"]
        contra = request.form["txtpass1"]

        cursor = con.cursor()

    if id:
    sql = " UPDATE tst0_usuarios SET Nombre_Usuario = %s, Contrasena     = %s WHERE Id_Usuario = %s"
    val = (nombre, contra, id)
else:
    if nombre and contra:  
        sql = "INSERT INTO tst0_usuarios (Id_Usuario, Nombre_Usuario, Contrasena) VALUES (%s, %s, %s)"
        val = (id, nombre, contra)


        
        # Inserción en la base de datos
        cursor.execute(sql, val)
        con.commit()

        Eventopusher()

        return make_response(jsonify({"success": True, "message": "Encuesta guardada exitosamente!"}))

    except mysql.connector.Error as err:
        print(f"Error al guardar la encuesta: {err}")
        return jsonify({"success": False, "message": f"Error al guardar la encuesta: {err}"}), 500

    finally:
        cursor.close()  # Asegúrate de cerrar el cursor
        con.close()     # Y también la conexión

if __name__ == "__main__":
    app.run(debug=True)
