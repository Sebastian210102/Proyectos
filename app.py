from flask import render_template
from flask import url_for
from flask import Flask
from flask import request,session,redirect
import sqlite3
from flask import Flask, request
import os
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)  # 16 bytes para una clave más segura


@app.route('/')
def landing():
    return render_template("landing.html")

@app.route('/funcionamiento')    
def funcionamiento():
    return render_template("funcionamiento.html")
    
@app.route('/soporte', methods=['GET','POST'])
def soporte():
    if request.method == 'POST':
        name=request.form.get("nombre")
        email=request.form.get("email")
        mensaje=request.form.get("mensaje")
        if name:
            if len(mensaje)>1:
                conexion=sqlite3.connect("mensaje.db")
                conexion.execute("INSERT INTO  mensaje (nombre,email,mensaje) values (?,?,?)", (name, email,mensaje))
                conexion.commit()
                conexion.close()
    return render_template("soporte.html")
    
@app.route('/productos')
def productos():
    return render_template("productos.html")
    
@app.route('/Login', methods=['GET', 'POST'])
def login():
    resultado = None

    if request.method == 'POST':
        email = request.form.get("correo")
        contrasena = request.form.get("contrasena")

        # Conectar a la base de datos
        conexion = sqlite3.connect("clientes.db")
        cursor = conexion.cursor()

        # Verificar si el usuario existe en la base de datos
        cursor.execute("SELECT * FROM clientes WHERE correo=?", (email,))
        usuario = cursor.fetchone()

        if usuario:
            # Usuario existe, verificar la contraseña
            if usuario[2] == contrasena:  # Suponiendo que la contraseña está en la tercera columna
                session['usuario'] = email
                conexion.close()
                return redirect(url_for('pagina_privada'))
                
            else:
                resultado = "Contraseña incorrecta"
        else:
            # Usuario no existe, registrar
            cursor.execute("INSERT INTO clientes (correo, contrasena) VALUES (?, ?)", (email, contrasena))
            conexion.commit()
            conexion.close()
            resultado = "Usuario registrado exitosamente"

    return render_template("Login.html", resultado=resultado)

@app.route("/crearBase")
def initBase():
    conexion = sqlite3.connect("clientes.db")
    try:
        conexion.execute("""CREATE TABLE IF NOT EXISTS clientes (
            codigo INTEGER PRIMARY KEY,
            correo TEXT,
            contrasena TEXT
        )""")
        conexion.commit()
        print("Se creó la tabla 'clientes'")
    except sqlite3.OperationalError as e:
        print("Error al crear la tabla 'clientes':", e)
    conexion.close()
    return "<h1>Éxito</h1>"

@app.route("/clientes")
def todosMisClientes():
    conexion = sqlite3.connect("clientes.db")
    cursor = conexion.execute("SELECT codigo, correo, contrasena FROM clientes")
    strlistaContactos = "<h1>Todos los Clientes</h1>"

    for fila in cursor:
        print(fila)
        strlistaContactos += "<br> %s, %s, %s" % fila

    conexion.close()

    return strlistaContactos

@app.route("/preguntas")
def preguntas():
    return render_template('Preguntas.html')
    
@app.route("/crearBase2")
def initBase2():
    conexion=sqlite3.connect("mensaje.db")
    try:
        conexion.execute("""CREATE TABLE IF NOT EXISTS mensaje (
                                    codigo INTEGER PRIMARY KEY,
                                  nombre TEXT,
                                  email TEXT,
                                  mensaje TEXT
             )""")
        conexion.commit()
        print("Se creó la tabla 'mensaje'")
    except sqlite3.OperationalError as e:
        print("Error al crear la tabla 'mensaje':", e)
    conexion.close()
    return "<h1>Éxito</h1>"
    
@app.route("/mensajes")
def todosMisMensajes():
    conexion=sqlite3.connect("mensaje.db")
    cursor=conexion.execute("SELECT codigo,nombre,email, mensaje from mensaje")
    strlistaMensajes="<h1>Todos los Mensajes</h1>"
    for fila in cursor:
        print(fila)
        strlistaMensajes+="<br> %s , %s , %s , %s "%fila
    conexion.close()

    return strlistaMensajes

@app.route('/pagina_privada')
def pagina_privada():
    if 'usuario' in session:
        usuario = session['usuario']
        return render_template('pagina_privada.html', usuario=usuario)
    else:
        return redirect(url_for('login'))


# Configuración de SQLite y creación de la tabla sensor_data
conn = sqlite3.connect('arduino_data.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        temperatura REAL,
        color TEXT,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()
conn.close()

@app.route('/temperaturas')
def temperatura():
    conn = sqlite3.connect('arduino_data.db')
    cursor = conn.cursor()

    # Obtener los últimos 10 registros de la base de datos
    cursor.execute('SELECT * FROM sensor_data ORDER BY fecha DESC LIMIT 10')
    data = cursor.fetchall()

    conn.close()

    return render_template('temperatura.html', data=data)

@app.route('/save_data', methods=['GET'])
def save_data():
    try:
        temperatura = request.args.get('temperatura')
        color = request.args.get('color')

        conn = sqlite3.connect('arduino_data.db')
        cursor = conn.cursor()

        # Insertar datos en la base de datos
        cursor.execute("INSERT INTO sensor_data (temperatura, color) VALUES (?, ?)", (temperatura, color))
        conn.commit()

        conn.close()

        return "Datos guardados correctamente"
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)


