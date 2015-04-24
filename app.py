from flask import Flask, render_template, request, redirect, session
import database

app = Flask(__name__)
app.secret_key = "YOLOSWAG"



@app.route('/testDB')
def testDB():
	cur.execute("SELECT sno FROM test")
	print cur.fetchall()
	return 'hi'


@app.route('/')
def library_system():
	school_name = 'Georgia Tech'
	return render_template('index.html', school_name = school_name)


@app.route('/hello', methods=['POST', 'GET'])
def hello_world():
	if request.method == 'GET':
		name = 'Pujun GET'
		return render_template('hello.html', name=name)
	elif request.method == 'POST':
		name = 'Pujun POST'
		return render_template('hello.html', name=name)
	else:
		return 'wtf'


@app.route('/register/', methods=['POST', 'GET'])
def register_user():
	f = request.form
	if f['password'] != f['confirm_password']:
		return render_template('index.html', register_error="Passwords don't match")

	u = database.new_user(f['username'], f['password'])
	print u
	session['username'] = u
	return redirect('/create-profile/')


@app.route('/login/',  methods=['POST', 'GET'])
def login():
	if request.method == 'GET':
		return render_template('index.html')
	elif request.method == 'POST':
		f = request.form
		if database.login(f['username'], f['password']):
			session['username'] = f['username']
			user = database.get_user(f['username'])
			if user[2]: # user is staff
				return render_template('staff-dashboard.html')
			else:
				return redirect('/search-books/')
		else:
			return render_template('index.html', login_error='Invalid username and password')
	else:
		return 'wtf!'


@app.route('/create-profile/', methods=['POST','GET'])
def create_profile():
	if request.method == 'GET':
		return render_template('create-profile.html')	
	elif request.method == 'POST':
		f = request.form
		username = session.get("username", None)
		print "SEE THIS ", username
		if database.create_profile(username, f['first-name'] + f['last-name'], f['dob'], f['gender'], f['email'], f['is-faculty'], f['address'], f['department']):
			return redirect('/search-books/')
		else:
			return render_template('index.html', login_error='Invalid username and password')
		# return logged in view
		return 'logged in!'
	else:
		return 'wtf!'


@app.route('/search-books/', methods=['POST','GET'])
def search_books():
	if request.method == 'GET':
		return render_template('search-books.html')

	elif request.method == 'POST':
		f = {}
		# clean form
		for k,v in request.form.items():
			f[k] = v.strip()
			if f[k] == '': f[k] = None
		if f['isbn'] != None: f['isbn'] = int(f['isbn'])

		# validate
		if f['isbn'] == None and f['title'] == None and f['author'] == None:
			return render_template('search-books.html', search_error="Either ISBN, Title, or Author must be filled.")
		
		#search
		print "HELLLLLO"
		checkout_books = database.search_books(
			isbn=f['isbn'],
			title=f['title'],
			author=f['author'],
			publisher=f['publisher'],
			edition=f['edition'], 
			reserved= 0)

		reserved_books = database.search_books(
			isbn=f['isbn'],
			title=f['title'],
			author=f['author'],
			publisher=f['publisher'],
			edition=f['edition'], 
			reserved= 1)

		# return render_template('search-results.html', books=books)
		session['checkout_books'] = checkout_books
		session['reserved_books'] = reserved_books
				
		print checkout_books, "BOOKS"
		return redirect('/request-hold/')
	else:
		return 'wtf!'



@app.route('/book-confirmation', methods=['GET', 'POST'])
def book_confirmation():
	# print "this is the beginning"
	# if request.method == 'POST':
	# 	print "THIS IS GEORGIAAAA"
	# 	print "hello bitches"
	# 	print "hello", request.form['selected-book-isbn']
	# 	database.create_issue(f['selected-book-isbn'], f['selected-book-isbn'], f['selected-book-isbn'])		
	# 	return render_template("book-confirmation.html", issue_id = issue_id)
	# else:
	# 	return render_template("book-confirmation.html")
	if request.method == 'GET':
		name = 'Pujun GET'
		return render_template('book-confirmation.html', name=name)
	elif request.method == 'POST':
		print "THIS IS GEORGIAAA"
		print "hello bitches"
		name = "chill dude"
		f = request.form
		print f.values
		database.create_issue(f['selected-book-isbn'], f['hold-request-date'], f['estimated-return-date'])
		return render_template('book-confirmation.html', issue_id=name)
	else:
		return 'wtf' 




@app.route('/request-extension')
def request_extension():
	return render_template('request-extension.html')


@app.route('/future-hold-request')
def future_hold_request():
	return render_template('future-hold-request.html')

@app.route('/track-book-location')
def track_book_location():
	return render_template('track-book-location.html')


@app.route('/request-hold/', methods=['GET', 'POST'])
def hold_request():
	if request.method == 'GET':
		checkout_books = session.get("checkout_books", None)
		reserved_books = session.get("reserved_books", None)
		return render_template('request-hold.html', checkout_books = checkout_books, reserved_books = reserved_books)
	elif request.method == 'POST':
		print 'posting'
		f = request.form
		database.hold_request(f['selected-book-isbn'], session['username'])
		message = "You have successfully requested a hold on the selected book"
		return render_template('search-books.html', message = message)
	else:
		return 'wtf!'


@app.route('/book-checkout/', methods=['POST'])
def book_checkout():
	f = request.form
	print f.items()
	issue_id = database.book_checkout(
		isbn=f['isbn'],
		copy_number=f['copy-number'],
		username=f['username'])
	return render_template('staff-dashboard.html', checkout_message="Issue id: " + str(issue_id))


@app.route('/return-book/', methods=['GET', 'POST'])
def return_book_screen():
	if request.method == 'GET':
		return "return-book-screen.html"
	elif request.method == "POST":
		f = request.form
		issue_id = f['issue-id']
		is_damaged = False
		if 'is-damaged' in f: is_damaged = True
		issue_details = []
		issue_details = database.return_book(issue_id, is_damaged)
		return render_template('staff-dashboard.html', return_book_message="Returned!", issue_details=issue_details)
	else:
		return "wtf"


@app.route('/lost-damaged-book')
def lost_damaged_book():
	return render_template('lost-damaged-book.html')


@app.route('/popular-books-report')
def popular_books_report():
	return render_template('popular-books-report.html')

@app.route('/frequent-users-report')
def frequent_users_report():
	return render_template('frequent-users-report.html')

@app.route('/popular-subjects-report')
def frequent_subjects_report():
	return render_template('popular-subjects-report.html')


@app.route('/damaged-books-report', methods=['POST', 'GET'])
def damaged_books_report():
	#find all the subjects
	subjects = database.get_subjects();
	subject_list = [s[0] for s in subjects]
	print subject_list
	if request.method == 'GET':	
		return render_template('damaged-books-report.html', subjects = subject_list)
	elif request.method == 'POST':
		table_contents = [];
		f = request.form
		print "this is sparta"
		print f['subject_1']
		# print f['month']
		print f.items()
		table_contents.append((f['subject_1'], database.find_num_damaged_books(f['month'], f['subject_1'])))
		table_contents.append((f['subject_2'], database.find_num_damaged_books(f['month'], f['subject_2'])))
		table_contents.append((f['subject_3'], database.find_num_damaged_books(f['month'], f['subject_3'])))
		print "THINGS THAT WILL GO IN THE TABLE", table_contents
		return render_template('damaged-books-report.html', subjects = subject_list, table_contents = table_contents, month = f['month'])
		
if __name__ == '__main__':
	app.run(debug=True)