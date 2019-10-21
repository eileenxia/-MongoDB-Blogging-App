import pymongo  # mongodb connector
from pprint import pprint
import datetime
from datetime import date

server = "mongodb://" + str()  +":" + str() +  "@cluster0-shard-00-00-ppp7l.mongodb.net:27017,cluster0-shard-00-01-ppp7l.mongodb.net:27017,cluster0-shard-00-02-ppp7l.mongodb.net:27017/"+ str() + "?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin"
# server = "mongodb://localhost"

try:  # initialize db connection
    connection = pymongo.MongoClient(server)

    print("Connection established.")

    #connection.server_info()  # force connection on a request as the
    # connect=True parameter of MongoClient seems
    # to be useless here
except pymongo.errors.ServerSelectionTimeoutError as err:
    print("Connection failure:")
    print(err)

# Fetch list of all databases
print('DB\'s present on the system:')
for dbn in connection.list_database_names():
    print('    %s' % dbn)

db = connection.test
print("connected to db")

# get handle for test collection
collection = db.testcoll
print("connected to db.testcoll")

try:
    print("create some entries")  # from pyMongo docs
    post1 = {"author": "Pat",
             "text": "Say hello to my new blog!",
             "tags": ["mongodb", "pymongo", "python"],
             "date": datetime.datetime.utcnow()}
    post_id = collection.insert_one(post1).inserted_id
    print("post_id 1: {}".format(post_id))
    post2 = {"author": "Pat",
             "text": "The second post!",
             "tags": ["mongodb", "pymongo", "python", "examples"],
             "date": datetime.datetime.utcnow()}
    post_id = collection.insert_one(post2).inserted_id
    print("post_id 2: {}".format(post_id))

except Exception as e:
    print("Error trying to write to collection:", type(e), e)

print(" find them all using a cursor AND pretty:")
try:
    iter = collection.find()
    print("back from find")
    for item in iter:
        # Show all the ObjectId's along just for fun
        print("ObjectId: {} ".format(item.get('_id')), end='')
        pprint(item)
except Exception as e:
    print("Error trying to read collection:", type(e), e)

print("cleaning up")
collection.drop()
print("\nConnection closed.")
