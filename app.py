from flask import Flask, request, jsonify
import psycopg2
import os
import socket
from urllib.parse import urlparse

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

# Extraer host del URL de conexión
parsed_url = urlparse(DATABASE_URL)
host = parsed_url.hostname

try:
    # Intentar resolver IPv4
    ipv4_host = socket.getaddrinfo(host, None, socket.AF_INET)[0][4][0]
    print(f"Conectando a Supabase (IPv4): {ipv4_host}")
    DATABASE_URL_IPV4 = DATABASE_URL.replace(host, ipv4_host)
except Exception as e:
    print(f"⚠️ No se pudo resolver IPv4, usando host original: {e}")
    DATABASE_URL_IPV4 = DATABASE_URL

# Conectar con IPv4 (o fallback)
import psycopg2
conn = psycopg2.connect(DATABASE_URL_IPV4, sslmode="require")


@app.route('/')
def home():
    return "¡Conexión exitosa con Supabase y Flask!"


# ---------------- CRUD ---------------- #

# CREATE - Agregar estudiante
@app.route('/estudiantes', methods=['POST'])
def crear_estudiante():
    data = request.get_json()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO estudiantes (numero_ma, nombre, apellido_ma, apellido_pa, fecha_nacin, email, telefono, fecha_ingre, estatus)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        data['numero_ma'], data['nombre'], data['apellido_ma'], data['apellido_pa'],
        data['fecha_nacin'], data['email'], data['telefono'], data['fecha_ingre'], data['estatus']
    ))
    conn.commit()
    cur.close()
    return jsonify({"message": "Estudiante creado correctamente"}), 201


# READ - Obtener todos los estudiantes
@app.route('/estudiantes', methods=['GET'])
def listar_estudiantes():
    cur = conn.cursor()
    cur.execute("SELECT * FROM estudiantes;")
    rows = cur.fetchall()
    cur.close()
    return jsonify(rows)


# UPDATE - Modificar estudiante
@app.route('/estudiantes/<numero_ma>', methods=['PUT'])
def actualizar_estudiante(numero_ma):
    data = request.get_json()
    cur = conn.cursor()
    cur.execute("""
        UPDATE estudiantes
        SET nombre=%s, apellido_ma=%s, apellido_pa=%s, fecha_nacin=%s, email=%s, telefono=%s, fecha_ingre=%s, estatus=%s
        WHERE numero_ma=%s
    """, (
        data['nombre'], data['apellido_ma'], data['apellido_pa'], data['fecha_nacin'],
        data['email'], data['telefono'], data['fecha_ingre'], data['estatus'], numero_ma
    ))
    conn.commit()
    cur.close()
    return jsonify({"message": "Estudiante actualizado correctamente"})


# DELETE - Eliminar estudiante
@app.route('/estudiantes/<numero_ma>', methods=['DELETE'])
def eliminar_estudiante(numero_ma):
    cur = conn.cursor()
    cur.execute("DELETE FROM estudiantes WHERE numero_ma = %s", (numero_ma,))
    conn.commit()
    cur.close()
    return jsonify({"message": "Estudiante eliminado correctamente"})

@app.route('/ver_estudiantes')
def ver_estudiantes():
    cur = conn.cursor()
    cur.execute("SELECT * FROM estudiantes;")
    rows = cur.fetchall()
    cur.close()

    html = "<h2>Lista de Estudiantes</h2>"
    html += "<table border='1' cellpadding='5'><tr>"
    html += "<th>Numero MA</th><th>Nombre</th><th>Apellido Materno</th><th>Apellido Paterno</th>"
    html += "<th>Fecha Nac.</th><th>Email</th><th>Telefono</th><th>Fecha Ingreso</th><th>Estatus</th></tr>"

    for r in rows:
        html += f"<tr>{''.join([f'<td>{c}</td>' for c in r])}</tr>"

    html += "</table>"
    return html


if __name__ == '__main__':
    app.run()



