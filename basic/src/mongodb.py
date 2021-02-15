""" 
https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
install mongo driver 4 python: python3 -m pip install pymongo 
""" 
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb: pymongo.database
mycol: pymongo.collection

""" create a database """
dblist = myclient.list_database_names()
if "mydatabase" in dblist:
  print("The database exists.")
else: 
   mydb = myclient["mydatabase"]

""" create a collection == table """
collist = mydb.list_collection_names()
if "customers" in collist:
  print("The collection exists.")
else:
   mycol = mydb["customers"]

""" insert in collection """
# If you do not specify an _id field, then MongoDB will add one for you and assign a unique id for each document.
mydict = { "name": "John", "address": "Highway 37" }
# insert one
x = mycol.insert_one(mydict)
print(x.inserted_id)
# insert many
mylist = [
  { "_id": 1, "name": "John", "address": "Highway 37"},
  { "_id": 2, "name": "Peter", "address": "Lowstreet 27"},
  { "_id": 3, "name": "Amy", "address": "Apple st 652"},
  { "_id": 4, "name": "Hannah", "address": "Mountain 21"},
  { "_id": 5, "name": "Michael", "address": "Valley 345"},
  { "_id": 6, "name": "Sandy", "address": "Ocean blvd 2"},
  { "_id": 7, "name": "Betty", "address": "Green Grass 1"},
  { "_id": 8, "name": "Richard", "address": "Sky st 331"},
  { "_id": 9, "name": "Susan", "address": "One way 98"},
  { "_id": 10, "name": "Vicky", "address": "Yellow Garden 2"},
  { "_id": 11, "name": "Ben", "address": "Park Lane 38"},
  { "_id": 12, "name": "William", "address": "Central st 954"},
  { "_id": 13, "name": "Chuck", "address": "Main Road 989"},
  { "_id": 14, "name": "Viola", "address": "Sideway 1633"}
]
x = mycol.insert_many(mylist)
print(x.inserted_ids)

""" selection """
# find first inserted document
x = mycol.find_one()
print(x)
# find all by id (insertion order)
for x in mycol.find():
   print(x)
# exclude fields
for x in mycol.find({},{ "_id": 0, "name": 1, "address": 1 }):
   print(x)
for x in mycol.find({},{ "address": 0 }):
   print(x)
# limit number of results
myresult = mycol.find().limit(5)
for x in myresult:
  print(x) 
# query w/equality
myquery = { "address": "Park Lane 38" }
# query starting w/S and superior
myquery = { "address": { "$gt": "S" } }
# query starting w/S
myquery = { "address": { "$regex": "^S" } }
mydoc = mycol.find(myquery)
for x in mydoc:
   print(x)

# sorting results, ascending by default
mydoc = mycol.find().sort("name") # == sort("name", 1)
mydoc = mycol.find().sort("name", -1) # descending 
for x in mydoc:
   print(x)

""" deleting """
myquery = { "address": "Mountain 21" }
mycol.delete_one(myquery)
myquery = { "address": {"$regex": "^S"} }
x = mycol.delete_many(myquery)
print(x.deleted_count, " documents deleted.") 
# delete all in the collection
x = mycol.delete_many({})
print(x.deleted_count, " documents deleted.")

""" updating """
myquery = { "address": "Valley 345" }
newvalues = { "$set": { "address": "Canyon 123" } }
mycol.update_one(myquery, newvalues)
for x in mycol.find():
   print(x)
# update several
myquery = { "address": { "$regex": "^S" } }
newvalues = { "$set": { "name": "Minnie" } }
x = mycol.update_many(myquery, newvalues)
print(x.modified_count, "documents updated.")

""" drop a collection """
mycol = mydb["customers"]
mycol.drop() 