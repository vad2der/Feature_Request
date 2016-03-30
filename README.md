Feature Request App
===================

How To Run:
-------------
Python should be installed on the system to use `pip` for modules installation.
Clone the repository. Git has to be installed. In Git Bash navigate to the folder you would like to store the repository (use `cd` command) type:
`git clone https://github.com/vad2der/Feature_Request`

Recomentadion is to use virtual environment. Traditionally, it is to be installed in a folder right beside our repository.
Once been installed, activate it. This app uses python 2.7. 

navigate into repository folder:
`cd Feature_Request`

install necessary python modules by:
`pip install -r requirements.txt`

To run the app type:
`python app.py`

Database of choise was SQLight to simplify usage - no database server has to be installed and run.
Open a browser. Application is built on Flask, and by default hostname will be: `http://127.0.0.1:5000/`

`username = testUser01`
`password = testUser01`


Requirements:
-------------

Build a web application that allows the user to create "feature requests".

A "feature request" is a request for a new feature that will be added onto an existing piece of software. Assume that the user is an employee at IWS who would be entering this information after having some correspondence with the client that is requesting the feature. The necessary fields are:

* **Title:** A short, descriptive name of the feature request.
* **Description:** A long description of the feature request.
* **Client:** A selection list of clients (use "Client A", "Client B", "Client C")
* **Client Priority:** A numbered priority according to the client (1...n). Client Priority numbers should not repeat for the given client, so if a priority is set on a new feature as "1", then all other feature requests for that client should be reordered.
* **Target Date:** The date that the client is hoping to have the feature.
* **Ticket URL:** A field for storing any URL
* **Product Area:** A selection list of product areas (use 'Policies', 'Billing', 'Claims', 'Reports')

ToDo list:
----------

* ~~Set database & _models_~~

1. ~~SQLight~~
2. ~~SQLAlchemy~~

* ~~Create _bdObject_ class as a separate layer to manupulate database from app~~

1. ~~SQLAlchemy~~
2. ~~_models_~~

* ~~Make webb app~~

1. ~~Flask~~
2. ~~Flask_resful~~
3. ~~_bdObject_~~

* ~~Make Front-End~~

1. ~~templates (HTML, jinja)~~
2. ~~scripts (JavaScript, jQuery)~~

* ~~Wrap app in login~~

1. ~~don't forget to put a secret_key~~