from flask import Flask, request, render_template
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
    return render_template("index.html")
       
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

@app.route("/districts/<int:state_id>")
def districts_by_state(state_id):

    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM districts
        WHERE state_id = %s
        ORDER BY district_name
    """, (state_id,))

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
@app.route("/subdistricts/<int:district_id>")
def subdistricts_by_district(district_id):

    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM subdistricts
        WHERE district_id = %s
        ORDER BY subdistrict_name
    """, (district_id,))

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
@app.route("/villages-by-subdistrict/<int:subdistrict_id>")
def villages_by_subdistrict(subdistrict_id):

    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM villages
        WHERE subdistrict_id = %s
        ORDER BY village_name
    """, (subdistrict_id,))

    rows = cur.fetchall()

    result = []

    for row in rows:
        result.append({
            "id": row[0],
            "village_code": row[1],
            "village_name": row[2]
        })

    cur.close()

    return result
@app.route("/village/<int:village_id>")
def village_details(village_id):

    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM villages
        WHERE id = %s
    """, (village_id,))

    row = cur.fetchone()

    cur.close()

    if row is None:
        return {
            "success": False,
            "message": "Village not found"
        }, 404

    return {
        "id": row[0],
        "village_code": row[1],
        "village_name": row[2],
        "subdistrict_id": row[3]
    }
@app.route("/villages")
def villages():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 20))
    offset = (page - 1) * limit
    subdistrict_id = request.args.get("subdistrict_id")

    cur = conn.cursor()

    if subdistrict_id:
        cur.execute("""
            SELECT *
            FROM villages
            WHERE subdistrict_id = %s
            ORDER BY village_name
            LIMIT %s OFFSET %s
        """, (subdistrict_id, limit, offset))
    else:
        cur.execute("""
            SELECT *
            FROM villages
            ORDER BY village_name
            LIMIT %s OFFSET %s
        """, (limit, offset))

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

@app.route("/stats")
def stats():

    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM states")
    states_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM districts")
    districts_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM subdistricts")
    subdistricts_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM villages")
    villages_count = cur.fetchone()[0]

    cur.close()

    return {
        "states": states_count,
        "districts": districts_count,
        "subdistricts": subdistricts_count,
        "villages": villages_count
    }
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
@app.route("/analytics")
def analytics():

    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM states")
    states = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM districts")
    districts = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM subdistricts")
    subdistricts = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM villages")
    villages = cur.fetchone()[0]

    cur.execute("""
        SELECT district_name
        FROM districts
        ORDER BY district_name
        LIMIT 5
    """)
    top_districts = [row[0] for row in cur.fetchall()]

    cur.close()

    return {
        "summary": {
            "states": states,
            "districts": districts,
            "subdistricts": subdistricts,
            "villages": villages
        },
        "sample_districts": top_districts
    }

@app.route("/docs")
def docs():
    return {
        "endpoints": [
            "/health",
            "/states",
            "/districts",
            "/districts/<state_id>",
            "/subdistricts",
            "/subdistricts/<district_id>",
            "/villages?page=1&limit=20",
            "/villages-by-subdistrict/<subdistrict_id>",
            "/search?q=ari",
            "/stats"
        ]
    }

if __name__ == "__main__":
    app.run(debug=True)