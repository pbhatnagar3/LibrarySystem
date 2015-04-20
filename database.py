import mysql.connector as sql
from mysql.connector import errorcode

db = {}

def connect():
	db = sql.connect(user='group62', 
		password='_password', 
		host="cs4400-library-management.c0erkhridnqw.us-east-1.rds.amazonaws.com", 
		database="libpro")

# Other methods
# All sql goes in this file (except create table statements)

