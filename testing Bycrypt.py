import pyodbc

passwd = 'Sam13!'

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\ProjectMain\Database.accdb;')
cursor = conn.cursor()
sql = ("""
    SELECT UsersTbl.Password
    FROM UsersTbl
    WHERE (((UsersTbl.Username)=?));
""")
params = ("Test21")
database_hash = conn.execute(sql,params)
for row in database_hash:
    print (row)
    x = row

passwd = hash(passwd)
passwd = float(passwd)

if passwd == x:
    print("match")
else:
    print("not match")

print(passwd)
