## Warehouse backend
A simple warehouse program, written in python.

app/*   : A dash web-demo app to test the backend service.

data/*  : The data (.json) files.

server/ : Backend code.
</br>   -->  serverConfig.py : configuration of the server.
</br>   -->  dataAccess.py   : the functions to access the database (json files).
</br>   -->  dataService.py  : the service to handle database requests (from kafka-stream). 
</br>   -->  serverTest.py   : a simple test of backend service.

