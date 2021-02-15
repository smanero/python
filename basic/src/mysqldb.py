"""
https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
install mysql driver 4 python: python3 -m pip install mysql-connector-python
""" 
import mysql.connector

mydb = mysql.connector.connect(
   host="localhost"
   , user="yourusername"
   , password="yourpassword"
   #, database="mydatabase"
)

print(mydb)

mycursor = mydb.cursor()
""" create database """
mycursor.execute("SHOW DATABASES")
for x in mycursor:
   print(x) 
mycursor.execute("CREATE DATABASE mydatabase")

""" create table """
mycursor.execute("SHOW TABLES")
for x in mycursor:
   print(x) 
mycursor.execute("CREATE TABLE customers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))")

""" insert """
sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
val = ("John", "Highway 21")
mycursor.execute(sql, val)
mydb.commit()
print(mycursor.rowcount, "record inserted.")
print("1 record inserted, ID:", mycursor.lastrowid) 
# many rows
sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
val = [
  ('Peter', 'Lowstreet 4'),
  ('Amy', 'Apple st 652'),
  ('Hannah', 'Mountain 21'),
  ('Michael', 'Valley 345'),
  ('Sandy', 'Ocean blvd 2'),
  ('Betty', 'Green Grass 1'),
  ('Richard', 'Sky st 331'),
  ('Susan', 'One way 98'),
  ('Vicky', 'Yellow Garden 2'),
  ('Ben', 'Park Lane 38'),
  ('William', 'Central st 954'),
  ('Chuck', 'Main Road 989'),
  ('Viola', 'Sideway 1633')
]
mycursor.executemany(sql, val)
mydb.commit()
print(mycursor.rowcount, "was inserted.") 

""" select """
mycursor.execute("SELECT * FROM customers")
myresult = mycursor.fetchall()
for x in myresult:
   print(x)
mycursor.execute("SELECT * FROM customers")
myresult = mycursor.fetchone()
print(myresult)
# where clause
sql = "SELECT * FROM customers WHERE address ='Park Lane 38'"
mycursor.execute(sql)
myresult = mycursor.fetchall()
for x in myresult:
   print(x)
sql = "SELECT * FROM customers WHERE address LIKE '%way%'"
mycursor.execute(sql)
myresult = mycursor.fetchall()
# prevent sql injection
sql = "SELECT * FROM customers WHERE address = %s ORDER BY name" # DESC
adr = ("Yellow Garden 2", )
mycursor.execute(sql, adr)
myresult = mycursor.fetchall()
for x in myresult:
   print(x)
# limit y offset
mycursor.execute("SELECT * FROM customers LIMIT 5")
myresult = mycursor.fetchall()
for x in myresult:
   print(x) 
mycursor.execute("SELECT * FROM customers LIMIT 5 OFFSET 2")
myresult = mycursor.fetchall()
for x in myresult:
   print(x) 

sql = "SELECT \
  users.name AS user, \
  products.name AS favorite \
  FROM users \
  INNER JOIN products ON users.fav = products.id" # only both tables
# LEFT JOIN products ON users.fav = products.id" # all users but only prods with users
# RIGHT JOIN products ON users.fav = products.id" # all products but only users with prods
mycursor.execute(sql)
myresult = mycursor.fetchall()
for x in myresult:
   print(x) 

""" delete """
sql = "DELETE FROM customers WHERE address = 'Mountain 21'"
mycursor.execute(sql)
mydb.commit()
print(mycursor.rowcount, "record(s) deleted")
# prevent sql injection
sql = "DELETE FROM customers WHERE address = %s"
adr = ("Yellow Garden 2", )
mycursor.execute(sql, adr)
mydb.commit()
print(mycursor.rowcount, "record(s) deleted")

""" update """
sql = "UPDATE customers SET address = %s WHERE address = %s"
val = ("Valley 345", "Canyon 123")
mycursor.execute(sql, val)
mydb.commit()
print(mycursor.rowcount, "record(s) affected") 

""" drop """
sql = "DROP TABLE IF EXISTS customers"
mycursor.execute(sql) 
