from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('landing.html')

if __name__ == '__main__':
    app.run(debug=True)
    
@app.route('/login')
def login():
    return render_template('login.html')

@app.route("/crearBase")
def initBase():
    conexion = sqlite3.connect("clientes.db")
    try:
        conexion.execute("""CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            edad INTEGER,
            correo TEXT,
            posicion TEXT
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
    cursor = conexion.execute("SELECT id, nombre, edad, correo, posicion FROM clientes")
    strlistaContactos = "<h1>Todos los Clientes</h1>"

    for fila in cursor:
        print(fila)
        strlistaContactos += f"<br> ID: {fila[0]}, Nombre: {fila[1]}, Edad: {fila[2]}, Correo: {fila[3]}, Posición: {fila[4]}"

    conexion.close()

    return strlistaContactos

@app.route('/registrar', methods=['POST'])
def registrar():
    nombre = request.form['nombre']
    edad = request.form['edad']
    correo = request.form['correo']
    posicion = request.form['posicion']

    conexion = sqlite3.connect('clientes.db')
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO clientes (nombre, edad, correo, posicion)
        VALUES (?, ?, ?, ?)
    ''', (nombre, edad, correo, posicion))
    conexion.commit()
    conexion.close()

    return "Registro exitoso"

if __name__ == '__main__':
    app.run(debug=True)
    
@app.route('/preguntas')
def preguntas():
    return render_template('preguntas.html')

if __name__ == '__main__':
    app.run(debug=True)