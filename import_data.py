import pandas as pd
import psycopg2

file_path = r"D:\Desktop\all-india-villages-master-list-excel\dataset\Rdir_2011_02_HIMACHAL_PRADESH.xls"

df = pd.read_excel(file_path)

conn = psycopg2.connect(
    host="localhost",
    database="villageapi",
    user="postgres",
    password="2302"
)

cur = conn.cursor()

count = 0

for _, row in df.iterrows():

    count += 1

    if count % 100 == 0:
        print("Processed:", count)

    state_code = str(row["MDDS STC"])
    state_name = str(row["STATE NAME"])

    district_code = str(row["MDDS DTC"])
    district_name = str(row["DISTRICT NAME"])

    subdistrict_code = str(row["MDDS Sub_DT"])
    subdistrict_name = str(row["SUB-DISTRICT NAME"])

    village_code = str(row["MDDS PLCN"])
    village_name = str(row["Area Name"])

    # STATE

    cur.execute("""
        INSERT INTO states
        (state_code, state_name)
        VALUES (%s,%s)
        ON CONFLICT (state_code) DO NOTHING
    """, (
        state_code,
        state_name
    ))

    cur.execute("""
        SELECT id
        FROM states
        WHERE state_code=%s
    """, (
        state_code,
    ))

    state_id = cur.fetchone()[0]

    # DISTRICT

    cur.execute("""
        INSERT INTO districts
        (district_code,district_name,state_id)
        VALUES (%s,%s,%s)
        ON CONFLICT (district_code) DO NOTHING
    """, (
        district_code,
        district_name,
        state_id
    ))

    cur.execute("""
        SELECT id
        FROM districts
        WHERE district_code=%s
    """, (
        district_code,
    ))

    district_id = cur.fetchone()[0]

    # SUBDISTRICT

    cur.execute("""
        INSERT INTO subdistricts
        (subdistrict_code,subdistrict_name,district_id)
        VALUES (%s,%s,%s)
        ON CONFLICT (subdistrict_code) DO NOTHING
    """, (
        subdistrict_code,
        subdistrict_name,
        district_id
    ))

    cur.execute("""
        SELECT id
        FROM subdistricts
        WHERE subdistrict_code=%s
    """, (
        subdistrict_code,
    ))

    subdistrict_id = cur.fetchone()[0]

    # VILLAGE

    if village_code != "0":

        cur.execute("""
            INSERT INTO villages
            (village_code,village_name,subdistrict_id)
            VALUES (%s,%s,%s)
            ON CONFLICT (village_code) DO NOTHING
        """, (
            village_code,
            village_name,
            subdistrict_id
        ))

conn.commit()

print("Import Completed Successfully!")

cur.close()
conn.close()