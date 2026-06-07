from flask import Flask, request
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(
    host="localhost",
    database="villageapi",
    user="postgres",
    password="2302"
)

@app.route("/")
def home():
    return {
        "success": True,
        "message": "Village API Running"
    }

@app.route("/states")
def states():

    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM states
        ORDER BY state_name
    """)

    rows = cur.fetchall()

    result = []

    for row in rows:
        result.append({
            "id": row[0],
            "state_code": row[1],
            "state_name": row[2]
        })

    cur.close()

    return result

@app.route("/districts")
def districts():

    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM districts
        ORDER BY district_name
    """)

    rows = cur.fetchall()

    result = []

    for row in rows:
        result.append({
            "id": row[0],
            "district_code": row[1],
            "district_name": row[2],
            "state_id": row[3]
        })

    cur.close()

    return result
@app.route("/health")
def health():
    return {
        "status": "ok",
        "database": "connected"
    }
@app.route("/subdistricts")
def subdistricts():

    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM subdistricts
        ORDER BY subdistrict_name
    """)

    rows = cur.fetchall()

    result = []

    for row in rows:
        result.append({
            "id": row[0],
            "subdistrict_code": row[1],
            "subdistrict_name": row[2],
            "district_id": row[3]
        })

    cur.close()

    return result
@app.route("/villages")
def villages():

    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM villages
        ORDER BY village_name
        LIMIT 100
    """)

    rows = cur.fetchall()

    result = []

    for row in rows:
        result.append({
            "id": row[0],
            "village_code": row[1],
            "village_name": row[2],
            "subdistrict_id": row[3]
        })

    cur.close()

    return result
@app.route("/search")
def search():

    q = request.args.get("q", "")

    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM villages
        WHERE village_name ILIKE %s
        LIMIT 20
    """, (f"%{q}%",))

    rows = cur.fetchall()

    result = []

    for row in rows:
        result.append({
            "id": row[0],
            "village_code": row[1],
            "village_name": row[2],
            "subdistrict_id": row[3]
        })

    cur.close()

    return result
if __name__ == "__main__":
    app.run(debug=True)