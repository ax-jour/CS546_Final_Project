# Project Structure #
### libraries required ###
- flask
- flask_cors

### ./sql_scripts ###
Contains sql executing files when starting the program. Hence, each time the database will be **reset**.

### ./static ###
Contains js and css files for webpages

### ./templates ###
Contains HTML files that will be rendering by flask

### ./test ###
Ignore this dir

### database.py ###
Contains all database related scripts

### main.py ###
The entry of the flask program. Execute `` flask --app main run `` to run the server program

### vote.py ###
Contains voting related functions

### zkp_*.py ###
Contains zero-knowledge proof related functions
