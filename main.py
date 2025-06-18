from flask import Flask, request, jsonify
import pyodbc
import os

app = Flask(__name__)

# Azure SQL connection using environment variables (safe)
def get_db_connection():
    try:
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={os.environ['DB_SERVER']};"
            f"DATABASE={os.environ['DB_NAME']};"
            f"UID={os.environ['DB_USER']};"
            f"PWD={os.environ['DB_PASS']};"
        )
        return conn
    except Exception as e:
        print("Database connection error:", e)
        return None

# Sample route to receive form data and save to Azure SQL
@app.route('/submit_form', methods=['POST'])
def submit_form():
    data = request.get_json()
    
    uid = data.get('uid')
    name = data.get('name')
    dob = data.get('dob')
    gender = data.get('gender')
    phone = data.get('phone')
    city = data.get('city')
    district = data.get('district')
    symptoms = data.get('symptoms')

    conn = get_db_connection()
    if conn is None:
        return jsonify({'status': 'error', 'message': 'DB connection failed'})

    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO PatientRawSubmission (UID, Name, DOB, Gender, Phone, City, District, Symptoms)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            uid, name, dob, gender, phone, city, district, symptoms)
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Data inserted'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
