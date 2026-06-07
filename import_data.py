import pandas as pd
import psycopg2

file_path = r"D:\Desktop\all-india-villages-master-list-excel\dataset\Rdir_2011_11_SIKKIM.xls"

df = pd.read_excel(file_path)

conn = psycopg2.connect(
    host="localhost",
    database="villageapi",
    user="postgres",
    password="2302"
)

cur = conn.cursor()

for _, row in df.iterrows():

    subdistrict_code = str(row["MDDS Sub_DT"])
    village_code = str(row["MDDS PLCN"])
    village_name = str(row["Area Name"])

    cur.execute(
        "SELECT id FROM subdistricts WHERE subdistrict_code=%s",
        (subdistrict_code,)
    )

    subdistrict = cur.fetchone()

    if subdistrict and village_code != "0":

        cur.execute("""
            INSERT INTO villages
            (village_code, village_name, subdistrict_id)
            VALUES (%s,%s,%s)
            ON CONFLICT (village_code) DO NOTHING
        """, (
            village_code,
            village_name,
            subdistrict[0]
        ))

conn.commit()

print("Villages imported successfully!")

cur.close()
conn.close()