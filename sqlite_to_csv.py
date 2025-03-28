import sqlite3

con = sqlite3.connect("instance/global_airports_sqlite.db")

cur = con.cursor()

res = cur.execute("SELECT * FROM airports").fetchall()

print(res[0])

with open("airports2.csv", "a+") as out:
    for i in res:
        # airportname,cityname,airportcode,lat,long
        out.write(str(i[3]) + "," + str(i[4]) + "," + str(i[2]) + "," + str(i[15]) + "," + str(i[16]) + "\n")
