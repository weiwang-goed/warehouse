## Warehouse backend
A simple warehouse program, written in python.

app/*   : A dash web-demo app to test the backend service.

data/*  : The data (.json) files.

server/ : Backend code.
   -->  serverConfig.py : configuration of the server.
   -->  dataAccess.py   : the functions to access the database (json files).
   -->  dataService.py  : provide the service to handle database requests (from stream). 
   -->  serverTest.py   : a simple test of backend service.

