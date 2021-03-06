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
		print "number of copies", num_copies
		if num_copies[0][0] > 0:
			to_return.append(r + num_copies[0])
		print "THIS IS BEING RETURNED", to_return
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
	"""
	Returns -1 if checkout fails, or issue id if it succeeds
	"""
	print "Checking out"
	# check if student is debarred
	query = "SELECT Is_debarred from student_faculty WHERE Username=%s"
	cur = db.cursor()
	cur.execute(query, (username,))
	is_debarred, = cur.fetchone()
	cur.close()
	if is_debarred:
		print "is debarred"
		return -1

	# check if book is on hold or is damaged
	query = "SELECT Future_requester, Is_damaged, Hold_expiry, Is_on_hold FROM book_copy WHERE Isbn=%s AND Copy_number=%s"
	values = (isbn, copy_number)
	print query % values
	cur = db.cursor()
	cur.execute(query, values)
	future_requester, is_damaged, hold_expiry, is_on_hold = cur.fetchone()
	# print hold_expiry > datetime.now().date()
	cur.close()
	if is_on_hold:
		if (hold_expiry > datetime.now().date() and future_requester != username) or is_damaged:
			print "is on hold or is damaged"
			return -1

	# create new issue 
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

	# update book_copy - reset hold columns
	query = "UPDATE book_copy SET Is_on_hold=0, Is_checked_out=1 WHERE Isbn=%s AND Copy_number=%s"
	values = (isbn, copy_number)
	print query % values
	cur = db.cursor()
	cur.execute(query, values)
	db.commit()
	cur.close()
	return issue_id

def return_book(issue_id, is_damaged):
	# get issue details
	query = "SELECT Username, Return_date, Isbn, Copy_id FROM issue WHERE Issue_id=%s"
	cur = db.cursor()
	cur.execute( query, (issue_id,) )
	username, return_date, isbn, copy_number = cur.fetchone()
	cur.close()

	# update book_copy
	query = "UPDATE book_copy SET Is_checked_out=0, Is_damaged=%s WHERE Isbn=%s AND Copy_number=%s"
	cur = db.cursor()
	cur.execute(query, (is_damaged, isbn, copy_number))
	db.commit()
	cur.close()
	penalty = 0.5 * float((datetime.now().date() - return_date).days)
	if penalty > 0:
		query = "UPDATE student_faculty SET Penalty=Penalty+%s WHERE Username=%s"
		cur = db.cursor()
		cur.execute(query, (penalty, username))
		db.commit()
		cur.close()
	else:
		penalty = 0
		
	return (username, isbn, copy_number, return_date, penalty)



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

month_name = {
				'1': 'Jan',
				'2': 'Feb',
				'3': 'March',
				'4': 'April',
				'5': 'May',
				'6': 'June'
}

def month_name_finder(month):
	return month_name[str(month)]

def frequent_users(month):	
	to_return = []
	cur = db.cursor()
	query = "select username from issue where EXTRACT(MONTH FROM Date_of_issue) = %s group by username limit 5"
	values = (month,)
	cur.execute(query, values)
	result = cur.fetchall()
	print "POPULAR user FOR MONTH", month, " ", result
	for r in result:
		username = r[0]
		query = "select count(*) from issue where EXTRACT(MONTH FROM Date_of_issue) = %s and isbn = %s"
		values = (month, username)
		cur.execute(query, values)
		num_checkouts = cur.fetchall()[0][0]
		if num_checkouts >= 10:
			to_return.append((month_name_finder(month),username, num_checkouts))
	
	return to_return

def track_book(isbn):
	to_return = []
	cur = db.cursor()
	query = 'select Shelf_number from located_on where Isbn = %s'
	values = (isbn,)
	cur.execute(query, values)
	result = cur.fetchall()
	shelf_number = result[0][0]
	query = 'select Aisle_number, Floor_number from shelf where Shelf_number = %s'
	values = (shelf_number,)
	cur.execute(query, values)
	result = cur.fetchall()
	aisle_number = result[0][0]
	floor_number = result[0][1]
	query = 'select Subject_name from book where Isbn = %s'
	values = (isbn,)
	cur.execute(query, values)
	result = cur.fetchall()
	subject_name = result[0][0]
	to_return.append((floor_number, shelf_number, aisle_number, subject_name))
	print "THIS IS WHAT IS BEING RETURNED", to_return
	return to_return
	


def last_user(isbn, book_copy):
	cur = db.cursor()
	query = 'select Username from issue where isbn = %s and Copy_id = %s order by return_date DESC LIMIT 1'
	values = (isbn, book_copy)
	cur.execute(query, values)
	result = cur.fetchall()
	return result
	

def update_penalty(last_user, amount_to_be_charged):
	cur = db.cursor()
	query = "select penalty from student_faculty where name = %s"
	values = (last_user,)
	cur.execute(query, values)
	result = cur.fetchall()
	print "here is the result motherfucka ", result
	penalty = result[0][0]
	total_amount = int(amount_to_be_charged) + int(penalty)
	if amount_to_be_charged > 100:
		query = "UPDATE student_faculty SET Penalty=%s, Is_debarred = '1' WHERE Username = %s"
	else:
		query = "UPDATE student_faculty SET Penalty=%s WHERE Username = %s"
	values = (str(total_amount), last_user)
	print query % values
	cur.execute(query, values)
	db.commit()
	cur.close()


def popular_subjects(month):
	to_return = []
	cur = db.cursor()
	query = 'select Subject_name from issue, book where issue.isbn = book.isbn and  EXTRACT(MONTH FROM Date_of_issue) = %s group by Subject_name limit 3 '
	values = (month,)
	cur.execute(query, values)
	result = cur.fetchall()
	print "POPULAR user FOR MONTH", month, " ", result
	for r in result:
		subject_name = r[0]
		query = 'select count(*) from issue, book where issue.isbn = book.isbn and  EXTRACT(MONTH FROM Date_of_issue) = %s and Subject_name = %s '
		values = (month, subject_name)
		cur.execute(query, values)
		num_checkouts = cur.fetchall()[0][0]
		to_return.append((month_name_finder(month), subject_name, num_checkouts))
	return to_return

def find_popular_books(month):
	to_return = []
	cur = db.cursor()
	query = "select isbn from issue where EXTRACT(MONTH FROM Date_of_issue) = %s group by isbn limit 3"
	values = (month,)
	cur.execute(query, values)
	result = cur.fetchall()
	print "POPULAR BOOK FOR MONTH", month, " ", result
	for r in result:
		isbn = r[0]
		title =  find_book_from_isbn(isbn)
		query = "select count(*) from issue where EXTRACT(MONTH FROM Date_of_issue) = %s and isbn = %s"
		values = (month, isbn)
		cur.execute(query, values)
		num_checkouts = cur.fetchall()[0][0]
		print "number of checkouts", num_checkouts
		to_return.append((month_name_finder(month),title, num_checkouts))
	
	return to_return

def find_book_from_isbn(isbn):
	# print "ISBN is ", isbn
	cur = db.cursor()
	query = "select title from book where isbn = %s"
	values = (isbn,)
	cur.execute(query, values)
	return cur.fetchall()[0][0]

def get_subjects():
	cur = db.cursor()
	query = "SELECT Name FROM subject"
	cur.execute( query )
	result = cur.fetchall()
	print "AVAILABLE SUBJECTS ", result
	return result

def find_num_damaged_books(month, subject):
	print "MONTH ", month
	print "SUBJECT ", subject
	cur = db.cursor()
	query = "select COUNT(*) from (Select copy_number, isbn from book_copy) as T,  (SELECT Copy_id, isbn FROM issue WHERE EXTRACT(MONTH FROM Return_date)  = %s AND Isbn IN (SELECT Isbn FROM book WHERE Subject_name = %s)) as M where M.copy_id = T.copy_number and M.isbn = T.isbn";
	values = (month, subject)
	cur.execute(query, values)
	result = cur.fetchall()
	print "HERE IS THE RESULT", result
	return result

if __name__ == '__main__':
	createBooks()



	





