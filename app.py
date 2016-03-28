"""
to be implemented in Flask
currently it is a layer to call for db manupulations through dbObject layer
"""
from models import ClientName, ProductArea
import dbObject as db
from flask import Flask, Request, render_template, flash, url_for
from flask_restful import reqparse, abort, Api, Resource, fields, marshal_with


app = Flask(__name__)
api = Api(app)


class FeatureRequest_api(Resource):
    def get(self):
        pass

    def post(self):
       pass

    def delete(self):
        pass

    def update(self):
        pass


# start page
@app.route('/')
def requests_and_tickets():
    return render_template('request_and_tickets.html')


# ticket page
@app.route('/ticket/<int:ticket_id>')
def ticket(ticket_id):
    ticket = db.get_requests_by_id_list([ticket_id])[0]
    return render_template('ticket.html', ticket=ticket)

api.add_resource(FeatureRequest_api, '/api/ticket/<param>')


def get_root_url():
    url_root = ''
    try:
        url_root = str(Request.url_root)
        #print url_root
    except Exception as e:
        url_root = 'http://www.example.com/myapplication'
    return url_root

if __name__ == "__main__":

    # will drop existing and create new tables
    db.create_tables()
    # test entries
    db.insert_new("request_1", "description for request 1", ClientName.CLIENT_A, 1, '2016 05 01', get_root_url(), ProductArea.BILLING)
    db.insert_new("request_2", "description for request 2", ClientName.CLIENT_B, 2, '2016 05 02', get_root_url(), ProductArea.CLAIM)
    db.insert_new("request_3", "description for request 3", ClientName.CLIENT_C, 3, '2016 05 03', get_root_url(), ProductArea.POLICIES)
    app.run(debug=True)


