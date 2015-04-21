import traceback
from datetime import date, datetime, timedelta
import mysql.connector as sql
from mysql.connector import errorcode

db = sql.connect(user='group62', 
		password='_password', 
		host="cs4400-library-management.c0erkhridnqw.us-east-1.rds.amazonaws.com", 
		database="libpro")

def connect():	
	print "Connected!"

# Other methods
# All sql goes in this file (except create table statements)

def new_user(username, password):
	cur = db.cursor()
	query = "INSERT INTO user (Username,Password) VALUES(%s, %s)"
	print username, password
	cur.execute( query, (username,password) )
	db.commit()
	cur.close()
	return username
	
def login(username, password):
	print username, password
	cur = db.cursor()
	query = "SELECT * FROM user WHERE Username=%s AND Password=%s"
	cur.execute(query, (username, password))
	if cur.fetchone():
		return True
		cur.close()
	else:
		return False
		cur.close()
	
	

