from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Conexión con la base de datos Supabase
conn = psycopg2.connect(
    host=host_ipv4,
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    port=os.getenv("DB_PORT"),
    sslmode="require"
)

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

# -------------------------------------- #

if __name__ == '__main__':
    app.run()

