from flask import Flask, request, jsonify
from supabase import create_client, Client
import os

app = Flask(__name__)

# Credenciales de Supabase
SUPABASE_URL = "https://eruitxmpherlpvsfbxrc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVydWl0eG1waGVybHB2c2ZieHJjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE3NjQzNzcsImV4cCI6MjA3NzM0MDM3N30.82_viITSdsVW25lrEUhh0TfgInL8ZKoWl0UUCaBOC_k"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def home():
    return "✅ Conexión establecida con Supabase REST API y Flask"

# CREATE
@app.route('/estudiantes', methods=['POST'])
def crear_estudiante():
    data = request.get_json()
    response = supabase.table("estudiantes").insert(data).execute()
    return jsonify(response.data)

# READ
@app.route('/estudiantes', methods=['GET'])
def listar_estudiantes():
    response = supabase.table("estudiantes").select("*").execute()
    return jsonify(response.data)

# UPDATE
@app.route('/estudiantes/<numero_ma>', methods=['PUT'])
def actualizar_estudiante(numero_ma):
    data = request.get_json()
    response = supabase.table("estudiantes").update(data).eq("numero_ma", numero_ma).execute()
    return jsonify(response.data)

# DELETE
@app.route('/estudiantes/<numero_ma>', methods=['DELETE'])
def eliminar_estudiante(numero_ma):
    response = supabase.table("estudiantes").delete().eq("numero_ma", numero_ma).execute()
    return jsonify(response.data)

@app.route('/ver_estudiantes')
def ver_estudiantes():
    response = supabase.table("estudiantes").select("*").execute()
    rows = response.data

    html = "<h2>Lista de Estudiantes</h2>"
    html += "<table border='1' cellpadding='5'><tr>"
    html += "<th>Numero MA</th><th>Nombre</th><th>Apellido Materno</th><th>Apellido Paterno</th>"
    html += "<th>Fecha Nac.</th><th>Email</th><th>Telefono</th><th>Fecha Ingreso</th><th>Estatus</th></tr>"

    for r in rows:
        html += "<tr>" + "".join(f"<td>{r.get(k, '')}</td>" for k in r.keys()) + "</tr>"

    html += "</table>"
    return html


if __name__ == '__main__':
    app.run()





