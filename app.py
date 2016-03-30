"""
to be implemented in Flask
currently it is a layer to call for db manupulations through dbObject layer
"""
import dbObject as db
from flask import Flask, request, Request, render_template, url_for, redirect, flash
from flask_restful import Api, Resource, fields, marshal_with
import ast
import os
from functools import wraps

app = Flask(__name__)
api = Api(app)
app.secret_key = os.urandom(24)
ticket_fields = {"id": fields.Integer,
                 "title": fields.String,
                 "description": fields.String,
                 "client": fields.String,
                 "client_priority": fields.Integer,
                 "target_date": fields.DateTime,
                 "ticket_url": fields.String,
                 "product_area": fields.String}


class FeatureRequest_api(Resource):
    """
    REST class for Reature request operations
    """
    @marshal_with(ticket_fields)
    def get(self, param):
        """
        function for GET method
        :param param:
        :return:
        """
        if param == "all":            
            output = db.get_all()
            return output, 200


    def post(self, param):
        """
        function for POST method
        :param param:
        :return:
        """
        if param =="new":
            entries_to_downgrade = db.check_priorities_EL(request.form.get('client_priority'))
            if len(entries_to_downgrade) > 0:
                db.downgrade_priorities(entries_to_downgrade)
            db.insert_new(title=request.form.get('title'),
                          description=request.form.get('description'),
                          client=request.form.get('client'),
                          client_priority=request.form.get('client_priority'),
                          target_date=request.form.get('target_date'),
                          url_root=request.form.get('url_root'),
                          product_area=request.form.get('product_area'))
        return '', 201


    def delete(self, param):
        if param == 'delete':
            db.delete_entry(request.form.get('id'))
        gaps = db.get_gaps()
        if len(gaps) > 0:
            db.eleminate_gaps(gaps)
        return '', 204


    def put(self, param):
        if param == 'update':
            ticket_id = request.form.get('id')
            a = str(db.get_requests_by_id_list([ticket_id])[0])
            b = ast.literal_eval(a)            
            if b["client_priority"] == str(request.form.get('client_priority')):
                db.update_entry(id=request.form.get('id'),
				          title=request.form.get('title'),
                          description=request.form.get('description'),
                          client=request.form.get('client'),
                          client_priority=request.form.get('client_priority'),
                          target_date=request.form.get('target_date'),
                          url_root=request.form.get('url_root'),
                          product_area=request.form.get('product_area'))
            else:
                db.delete_entry(ticket_id)
                gaps = db.get_gaps()
                if len(gaps) > 0:
                    db.eleminate_gaps(gaps)
                entries_to_downgrade = db.check_priorities_EL(request.form.get('client_priority'))
                if len(entries_to_downgrade) > 0:
                    db.downgrade_priorities(entries_to_downgrade)
                db.insert_new(ind=request.form.get('id'),
				          title=request.form.get('title'),
                          description=request.form.get('description'),
                          client=request.form.get('client'),
                          client_priority=request.form.get('client_priority'),
                          target_date=request.form.get('target_date'),
                          url_root=request.form.get('url_root'),
                          product_area=request.form.get('product_area'))
        gaps = db.get_gaps()
        if len(gaps) > 0:
            db.eleminate_gaps(gaps)
        return '', 201


class Utils_api(Resource):
    def get(self, param):
        if param == "client_list":
            return db.get_client_list()
        if param == "possible_priorities":
            return db.get_possible_priorities()
        if param == "production_areas":
            return db.get_production_area_list()

    def post(self, param):
       pass

    def delete(self):
        pass

    def update(self):
        pass


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Log in first')
            return redirect(url_for('login'))
        return wrap


# start page
@app.route('/')
#@login_required
def requests_and_tickets():
    return render_template('request_and_tickets.html')


# ticket page
@app.route('/ticket/<int:ticket_id>')
#@login_required
def ticket(ticket_id):
    if ticket_id in db.get_all_ticket_ids():
        ticket = db.get_requests_by_id_list([ticket_id])[0]
        return render_template('ticket.html', ticket=ticket)
    else:
        return render_template('404ticket.html', ticket_id=ticket_id)


#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        if request.form['username'] != 'testUser01' or request.form['password'] != 'testUser01':
            error = 'Invalid username+password pair. CHeck your spelling or contact support.'
    else:
        session['logged_in'] = True
        return redirect(url_for('requests_and_tickets'))
    return render_template('login.html', error=error)


#logout
@app.route('/logout')
def logout():
    session.pop('logged_in')
    return render_template('login.html', error=None)

api.add_resource(FeatureRequest_api, '/api/ticket/<param>')
api.add_resource(Utils_api, '/api/<param>')


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
    #db.create_tables()
    # test entries
    #db.insert_new("request_1", "description for request 1", ClientName.CLIENT_A, 1, 'Sun, 01 May 2016', get_root_url(), ProductArea.BILLING)
    #db.insert_new("request_2", "description for request 2", ClientName.CLIENT_B, 2, 'Mon, 02 May 2016', get_root_url(), ProductArea.CLAIM)
    #db.insert_new("request_3", "description for request 3", ClientName.CLIENT_C, 3, 'Tue, 03 May 2016', get_root_url(), ProductArea.POLICIES)
    app.run(debug=True)


