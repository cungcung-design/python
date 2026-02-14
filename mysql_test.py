import mysql.connector

db = mysql.connector.connect(
    host ="Localhost",
    user= "root",
    password= "12345678",
    database = "classicmodel"
)

print("MySQL connected")

cursor = db.cursor()
cursor.execute("SELECT * FROM CUSTOMERS LIMIT 5")

for x in cursor:
    print(x)