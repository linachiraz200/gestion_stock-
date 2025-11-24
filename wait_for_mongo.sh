# wait_for_mongo.py
import socket
import time

mongo_host = 'mongo'
mongo_port = 27017

print("Waiting for MongoDB to start...")
while True:
    try:
        with socket.create_connection((mongo_host, mongo_port), timeout=2):
            print("MongoDB is up!")
            break
    except OSError:
        time.sleep(2)
