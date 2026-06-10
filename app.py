from unittest import result

from flask import Flask, request, render_template
import psycopg2
import uuid

app = Flask(__name__)

conn = psycopg2.connect(
    host="localhost",
    database="villageapi",
    user="postgres",
    password="2302"
)

def validate_api_key(api_key):

    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM api_keys
        WHERE api_key = %s
    """, (api_key,))

    key = cur.fetchone()

    cur.close()

    return key

def log_api_usage(user_id, endpoint):

    cur = conn.cursor()

    cur.execute("""
        INSERT INTO api_logs
        (user_id, endpoint)
        VALUES (%s, %s)
    """, (user_id, endpoint))

    conn.commit()

    cur.close()

@app.route("/")
def home():
    return render_template("index.html")
       
@app.route("/states")
def states():

    #api_key = request.args.get("api_key")

    # key_data = validate_api_key(api_key)

    # if not key_data:

    #     return {
    #         "success": False,
    #         "message": "Invalid API Key"
    #     }, 401
        
    #user_id = key_data[1]
    #log_api_usage(user_id, "/states")

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
        SELECT
         v.id,
         v.village_name,
         v.village_code,
         s.subdistrict_name,
         d.district_name,
         st.state_name
        FROM villages v
        JOIN subdistricts s
         ON v.subdistrict_id = s.id
        JOIN districts d
         ON s.district_id = d.id
        JOIN states st
         ON d.state_id = st.id
        WHERE subdistrict_id = %s
        ORDER BY village_name
    """, (subdistrict_id,))

    rows = cur.fetchall()

    result = []

    for row in rows:
      result.append({
        "id": row[0],
        "village_name": row[1],
        "village_code": row[2],
        "subdistrict": row[3],
        "district": row[4],
        "state": row[5]
    })

    cur.close()
    return result

@app.route("/village/<int:village_id>")
def village_details(village_id):

    cur = conn.cursor()

    cur.execute("""
        SELECT
            v.id,
            v.village_name,
            v.village_code,
            s.subdistrict_name,
            d.district_name,
            st.state_name
        FROM villages v
        JOIN subdistricts s
            ON v.subdistrict_id = s.id
        JOIN districts d
            ON s.district_id = d.id
        JOIN states st
            ON d.state_id = st.id
        WHERE v.id = %s  
    """, (village_id,))

    row = cur.fetchone()

    cur.close()

    if not row:
        return {"message": "Village not found"}, 404

    return {
        "id": row[0],
        "village_name": row[1],
        "village_code": row[2],
        "subdistrict": row[3],
        "district": row[4],
        "state": row[5]
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
        SELECT
            v.id,
            v.village_name,
            v.village_code,
            s.subdistrict_name,
            d.district_name,
            st.state_name
        FROM villages v
        JOIN subdistricts s
            ON v.subdistrict_id = s.id
        JOIN districts d
            ON s.district_id = d.id
        JOIN states st
            ON d.state_id = st.id
        WHERE v.village_name ILIKE %s
        LIMIT 20
    """, (f"%{q}%",))

    rows = cur.fetchall()

    result = []

    for row in rows:
        result.append({
            "id": row[0],
            "village_name": row[1],
            "village_code": row[2],
            "subdistrict": row[3],
            "district": row[4],
            "state": row[5]
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

@app.route("/register", methods=["POST"])
def register():

    data = request.json

    name = data["name"]
    email = data["email"]
    password = data["password"]

    cur = conn.cursor()

    cur.execute("""
        INSERT INTO users
        (name, email, password)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (name, email, password))

    user_id = cur.fetchone()[0]

    conn.commit()

    cur.close()

    return {
        "success": True,
        "user_id": user_id
    }

@app.route("/users")
def users():

    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, email, plan
        FROM users
        ORDER BY id
    """)

    rows = cur.fetchall()

    result = []

    for row in rows:

        result.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "plan": row[3]
        })

    cur.close()

    return result

@app.route("/create-test-user")
def create_test_user():

    cur = conn.cursor()

    cur.execute("""
        INSERT INTO users
        (name, email, password)
        VALUES
        (
            'Adi',
            'adi@test.com',
            '123456'
        )
        RETURNING id
    """)

    user_id = cur.fetchone()[0]

    conn.commit()

    cur.close()

    return {
        "user_id": user_id
    }

@app.route("/generate-key/<int:user_id>")
def generate_key(user_id):

    api_key = str(uuid.uuid4())

    cur = conn.cursor()

    cur.execute("""
        INSERT INTO api_keys
        (user_id, api_key)
        VALUES (%s, %s)
    """, (user_id, api_key))

    conn.commit()

    cur.close()

    return {
        "success": True,
        "api_key": api_key
    }

@app.route("/api-keys")
def api_keys():

    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM api_keys
        ORDER BY id
    """)

    rows = cur.fetchall()

    result = []

    for row in rows:

        result.append({
            "id": row[0],
            "user_id": row[1],
            "api_key": row[2]
        })

    cur.close()

    return result

@app.route("/api-logs")
def api_logs():

    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM api_logs
        ORDER BY id DESC
    """)

    rows = cur.fetchall()

    result = []

    for row in rows:

        result.append({
            "id": row[0],
            "user_id": row[1],
            "endpoint": row[2]
        })

    cur.close()

    return result

@app.route("/dashboard")
def dashboard():

    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM users")
    users_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM api_keys")
    keys_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM api_logs")
    logs_count = cur.fetchone()[0]

    cur.close()

    return {
        "total_users": users_count,
        "total_api_keys": keys_count,
        "total_requests": logs_count
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
            "/search?q=village_name",
            "/village/<village_id>",
            "/stats",
            "/users",
            "/api-keys",
            "/api-logs",
            "/dashboard"
        ]
    }

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/generate-key/<int:user_id>")
def generate_key(user_id):

    api_key = str(uuid.uuid4())

    cur = conn.cursor()

    cur.execute("""
        INSERT INTO api_keys
        (user_id, api_key)
        VALUES (%s, %s)
    """, (user_id, api_key))

    conn.commit()

    cur.close()

    return {
        "success": True,
        "api_key": api_key
    }

@app.route("/api-keys")
def api_keys():

    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM api_keys
        ORDER BY id
    """)

    rows = cur.fetchall()

    result = []

    for row in rows:

        result.append({
            "id": row[0],
            "user_id": row[1],
            "api_key": row[2]
        })

    cur.close()

    return result

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