"""
to be implemented in Flask
currently it is a layer to call for db manupulations through dbObject layer
"""
from models import ClientName, ProductArea
import dbObject as db

# will drop existing and create new tables
db.create_tables()

# test entries
db.insert_new("request_1", "description for request 1", ClientName.CLIENT_A, 1, '2016 05 01', ProductArea.BILLING)
db.insert_new("request_2", "description for request 2", ClientName.CLIENT_B, 2, '2016 05 02', ProductArea.CLAIM)
db.insert_new("request_3", "description for request 3", ClientName.CLIENT_C, 3, '2016 05 03', ProductArea.POLICIES)

for entry in db.get_all():
    print entry
