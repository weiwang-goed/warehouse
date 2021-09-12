## Warehouse backend
A simple warehouse program, written in python.

app/*   : A dash web-demo app to test the backend service.

data/*  : The data (.json) files.

server/ : Backend code.
\newline   -->  serverConfig.py : configuration of the server.
\newline   -->  dataAccess.py   : the functions to access the database (json files).
\newline   -->  dataService.py  : the service to handle database requests (from kafka-stream). 
\newline   -->  serverTest.py   : a simple test of backend service.

