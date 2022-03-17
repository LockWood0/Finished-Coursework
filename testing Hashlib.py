from hashlib import sha256
import pyodbc

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\ProjectMain\Database.accdb;')
cursor = conn.cursor()
sql = ("""
    SELECT UsersTbl.Password
    FROM UsersTbl
    WHERE (((UsersTbl.Username)=?));
""")
params = ("Mr_Curran")
database_hash = conn.execute(sql,params)
for row in database_hash:
    print (row)
    x = row

h = sha256()
h.update(b'!Th383$t')
hash = h.hexdigest()
print(hash)

if hash == x[0]:
    print("match")

else:
    print("not match")