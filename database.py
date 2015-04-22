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
	print query % (username, password)
	cur.execute( query, (username,password) )
	db.commit()
	cur.close()
	return username
	
def login(username, password):
	cur = db.cursor()
	query = "SELECT EXISTS(SELECT * FROM user WHERE Username=%s AND Password=%s)"
	cur.execute(query, (username, password))
	exists, = cur.fetchone() # fetchone returns a tuple
	if exists:
		return True
		cur.close()
	else:
		return False
		cur.close()

def get_user(username):
	cur = db.cursor()
	query = "SELECT * FROM user WHERE Username=%s"
	cur.execute( query, (username,) )
	return cur.fetchone()


def create_profile(username, name, dob, gender, email, is_faculty, address, department):
	cur = db.cursor()
	query = "INSERT into student_faculty values(%s, %s, %s, %s,%s, %s,%s, %s,%s, %s)"
	cur.execute(query, (username, name, dob, gender, 'false',email, address,  is_faculty, '100', department))
	db.commit()
	cur.close()
	return True

def search_books(isbn, title, author, publisher, edition, reserved):
	'''
	cur = db.cursor()
	if author is not None:
		query = "SELECT Isbn FROM author WHERE Name = %s" 
		values = (author,) 
		cur.execute(query,values)
		result = cur.fetchall()
		print "THIS IS THE RESULT" + result	
		return result
	'''	
	print "search_books"
	query = "SELECT * FROM book WHERE "
	params = {'Isbn':isbn, 
			'Title':title, 
			#'Author':author,
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
	if author is not None:
		query = query + " AND (Isbn IN (SELECT Isbn FROM author WHERE Name = %s))" 
		values.append(author)
	cur = db.cursor()
	print query % tuple(values)
	cur.execute( query, tuple(values) )
		# print "SEE THIS", cur.fetchall()
	result = cur.fetchall()
	to_return = []
	for r in result:
		# print r[0], "Getting Copies"
		cur.execute("SELECT count(Copy_number) from book_copy where Isbn = %s AND Is_checked_out = 0 AND Is_on_hold = 0" % (r[0]))
		num_copies = cur.fetchall()
		# print "number of copies", num_copies
		to_return.append(r + num_copies[0])
	return to_return

def create_issue(isbn, hold_request_date, estimated_return_date):
	print "ISBN", isbn
	print hold_request_date
	print estimated_return_date
	return True


def hold_request(isbn, future_requester):
	# When the submit button is clicked, select the lowest copy_number available of the selected ISBN
	query = "SELECT MIN(Copy_number) FROM book_copy WHERE Isbn=" + isbn + " AND Is_checked_out=0 AND Is_on_hold=0"
	print "hold request"
	cur = db.cursor()
	cur.execute(query)
	copy_number, = cur.fetchone()
	#TODO Add hold expiry
	expiry = datetime.now() + timedelta(days=3)
	query = "UPDATE book_copy SET Future_requester=%s, Is_on_hold=1, Hold_expiry=%s WHERE Isbn=%s AND Copy_number=%s"
	values = (future_requester, expiry, isbn, copy_number)
	print query % values
	cur.execute(query, values)
	db.commit()
	cur.close()

def book_checkout(isbn, copy_number, username):
	print "Checking out"
	issue_date = datetime.now()
	return_date = issue_date + timedelta(days=14)
	query = "INSERT into issue " + \
			"(Isbn, Copy_id, Username, Date_of_issue, Return_date, Extension_date, Count_of_extensions) " + \
			"values(%s, %s, %s, %s, %s, %s, %s)"
	values = (isbn, copy_number, username, issue_date, return_date, return_date, 0)
	print query % values
	cur = db.cursor()
	cur.execute(query, values)
	db.commit()
	issue_id = cur.lastrowid
	cur.close()
	return issue_id


def createBooks():
	'''
	TABLES['book'] = (
	"CREATE TABLE `book` ("
    "  `Isbn` varchar(50) NOT NULL,"
    "  `Title` varchar(100) NOT NULL,"
    "  `Is_reserved` BOOLEAN NOT NULL,"
    "  `Edition` INT,"
    "  `Publisher` varchar(100),"
    "  `Place_of_publication` VARCHAR(100),"
    "  `Copyright` SMALLINT,"
    "  `Subject_name` VARCHAR(50) NOT NULL,"
    "  `Cost` REAL NOT NULL,"

    "  PRIMARY KEY (`Isbn`),"
    "  FOREIGN KEY (`Subject_name`) REFERENCES subject (`Name`)"
    ") ENGINE=InnoDB")
	'''
	cur = db.cursor()
	books = ['ECE2026','ECE2020','ECE2040','ECE2035','ECE2036']
	isbn = ['2026','2020','2040','2035','2036']
	on_reserve = [0,0,1,1,0]
	for i in range(0,5):
		query = "INSERT INTO book VALUES(%s,%s,%s,1,%s,%s,1,%s,1000)"
		values = (isbn[i],books[i],on_reserve[i],"GaTech","Georgia","ECE")
		cur.execute(query,values)
		db.commit()
	'''
	TABLES['book_copy'] = (
	"CREATE TABLE `book_copy` ("
    "  `Future_requester` varchar(50),"
    "  `Hold_expiry` DATE,"
    "  `Is_damaged` BOOLEAN NOT NULL,"
    "  `Is_checked_out` BOOLEAN NOT NULL,"
    "  `Is_on_hold` BOOLEAN NOT NULL,"
    "  `Copy_number` INT,"
    "  `Isbn` VARCHAR(50) NOT NULL,"
    "  PRIMARY KEY (`Copy_number`, `Isbn`),"
    "  FOREIGN KEY (`Future_requester`) REFERENCES user (`Username`),"
    "  FOREIGN KEY (`Isbn`) REFERENCES book (`Isbn`)"
    ") ENGINE=InnoDB")
	'''
	for book in isbn:
		for i in range(1,5):
			query = "INSERT INTO book_copy(Is_damaged,Is_checked_out,Is_on_hold,Copy_number,Isbn) VALUES(0,0,0,%s,%s)"
			values = (i,book)
			cur.execute(query,values)
			db.commit()


	cur.close()	



if __name__ == '__main__':
	createBooks()



	





