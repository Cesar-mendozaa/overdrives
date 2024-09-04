from flask import Flask, request, jsonify, session
from datetime import datetime
import bcrypt, pyodbc
from flask_session import Session
from flask_cors import CORS


app = Flask(__name__)
app.config['SECRET_KEY'] = '1583497620HiJST53uB4'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
CORS(app, supports_credentials=True)


conexion = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=MATEBOOK-D15\SQLEXPRESS;"
    "DATABASE=Prueba DB;"
    "UID=luis;"
    "PWD=1583497620;"
)


def get_db_connection():
    return pyodbc.connect(conexion)


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')

    if not username or not phone or not password:
        return jsonify({"success": False, "message": "Nombre de usuario, teléfono y contraseña son obligatorios"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM Usuario WHERE user_name = ?", (username,))
        user_count = cursor.fetchone()[0]
        if user_count > 0:
            return jsonify({"success": False, "message": "El nombre de usuario ya existe. Por favor, elige otro nombre de usuario."}), 400

        cursor.execute("SELECT COUNT(*) FROM Usuario WHERE phone = ?", (phone,))
        phone_count = cursor.fetchone()[0]
        if phone_count > 0:
            return jsonify({"success": False, "message": "El teléfono ya está registrado. Por favor, utiliza otro teléfono."}), 400

        if email:
            cursor.execute("SELECT COUNT(*) FROM Usuario WHERE email = ?", (email,))
            email_count = cursor.fetchone()[0]
            if email_count > 0:
                return jsonify({"success": False, "message": "El correo electrónico ya está registrado. Por favor, utiliza otro correo electrónico."}), 400

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cursor.execute("""
            INSERT INTO Usuario (user_name, email, phone, password, register_date) 
            VALUES (?, ?, ?, ?, GETDATE(), ?)
        """, (username, email, phone, hashed_password))
        conn.commit()


    except pyodbc.IntegrityError as e:
        return jsonify({"success": False, "message": "Error de integridad: " + str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "message": "Error inesperado: " + str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    identifier = data.get('identifier')
    password = data.get('password')

    if not identifier or not password:
        return jsonify({"success": False, "message": "Nombre de usuario, teléfono o correo electrónico y contraseña son obligatorios"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT id_usuario, password FROM Usuario
            WHERE user_name = ? OR email = ? OR phone = ?
        """, (identifier, identifier, identifier))
        
        user = cursor.fetchone()
        
        if user:
            user_id, hashed_password = user
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                # print(f"User ID set in session: {session['user_id']}")

                session['user_id'] = user_id
                return jsonify({"success": True, "message": "Inicio de sesión exitoso"}), 200
            else:
                return jsonify({"success": False, "message": "Contraseña incorrecta"}), 401
        else:
            return jsonify({"success": False, "message": "Usuario no encontrado"}), 404
    except Exception as e:
        # print(e)
        return jsonify({"success": False, "message": "Error inesperado: " + str(e)}), 500
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)