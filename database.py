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
	query = "SELECT EXISTS(SELECT * FROM user WHERE Username=%s AND Password=%s)"
	cur.execute(query, (username, password))
	exists, = cur.fetchone()
	print exists
	if exists:
		return True
		cur.close()
	else:
		return False
		cur.close()
	
def create_profile(username, name, dob, gender, email, is_faculty, address, department):
	print name
	cur = db.cursor()
	query = "INSERT into student_faculty values(%s, %s, %s, %s,%s, %s,%s, %s,%s, %s)"
	cur.execute(query, (username, name, dob, gender, 'false',email, address,  is_faculty, '100', department))
	db.commit()
	cur.close()
	return True

def search_books(isbn, title, author, publisher, edition, reserved):
	query = "SELECT * FROM book WHERE "
	params = {'Isbn':isbn, 
		'Title':title, 
		'Author':author,
		'Publisher':publisher,
		'Edition':edition, 
		'Is_reserved': reserved}

	to_query = [a[0] for a in params.items() if a[1]!=None]
	values = [params[q] for q in to_query]
	# print to_query
	# print values

	for i,p in enumerate(to_query):
		if i > 0: query += ' AND ' + p + '=%s'
		else: query += p + '=%s'

	# print query, tuple(values)
	print "QUERY", query
	cur = db.cursor()
	cur.execute( query, tuple(values) )
	# print "SEE THIS", cur.fetchall()
	result = cur.fetchall()
	to_return = []
	print result, "here is the result"
	for r in result:
		cur.execute("SELECT count(Copy_number) from book_copy where Isbn = %s AND Is_checked_out = 0 AND Is_on_hold = 0" % (r[0]))
		num_copies = cur.fetchall()
		print "number of copies", num_copies
		to_return.append(r + num_copies[0])
	return to_return
