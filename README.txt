In the module send_email.py variables 'from_email' and 'from_password' need to be filled in.

To be able to run this app locally: 
 - A PostgreSQL server needs to be installed.
 - A database 'height_collector' (with user 'postgres') needs to be created.
 - Last step is to use terminal to create table 'data' in the database:
   >>> from Data_Collector_frontend import db
   >>> db.create_all()