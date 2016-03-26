"""
to be implemented in Flask
currently it is a layer to call for db manupulations through dbObject layer
"""
from models import ClientName, ProductArea
import dbObject as db
from flask import request

url_root = ''
try:
    url_root = request.url_root
except Exception as e:
    url_root = 'http://www.example.com/myapplication'

# will drop existing and create new tables
db.create_tables()

# test entries
db.insert_new("request_1", "description for request 1", ClientName.CLIENT_A, 1, '2016 05 01', url_root, ProductArea.BILLING)
db.insert_new("request_2", "description for request 2", ClientName.CLIENT_B, 2, '2016 05 02', url_root, ProductArea.CLAIM)
db.insert_new("request_3", "description for request 3", ClientName.CLIENT_C, 3, '2016 05 03', url_root, ProductArea.POLICIES)

for entry in db.get_all():
    print entry

a = db.check_priorities_EL(2)
print a

db.downgrade_priorities(a)

for entry in db.get_all():
    print entry

print db.get_possible_priorities()

b = db.get_gaps()

print b

db.eleminate_gaps(b)

for entry in db.get_all():
    print entry