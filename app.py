from flask import Flask, render_template, request, redirect
import database
	

app = Flask(__name__)


@app.route('/testDB')
def testDB():
	cur.execute("SELECT sno FROM test")
	print cur.fetchall()
	return 'hi'


@app.route('/')
def library_system():
	school_name = 'Georgia Tech'
	return render_template('index.html', school_name = school_name)


@app.route('/hello')
def hello_world():
	name = 'Pujun'
	return render_template('hello.html', name=name)


@app.route('/register/', methods=['POST', 'GET'])
def register_user():
	f = request.form
	if f['password'] != f['confirm_password']:
		return render_template('index.html', register_error="Passwords don't match")

	u = database.new_user(f['username'], f['password'])
	print u
	return redirect('/create-profile/')


@app.route('/login/', methods=['POST', 'GET'])
def login():
	if request.method == 'GET':
		return render_template('index.html')
	elif request.method == 'POST':
		print request.form['username'], request.form['password']
		# return logged in view
		return 'logged in!'
	else:
		return 'wtf!'


@app.route('/create-profile/')
def create_profile():
	return render_template('create-profile.html')


@app.route('/search-books')
def search_books():
	return render_template('search-books.html')


@app.route('/request-extension')
def request_extension():
	return render_template('request-extension.html')

@app.route('/future-hold-request')
def future_hold_request():
	return render_template('future-hold-request.html')

@app.route('/track-book-location')
def track_book_location():
	return render_template('track-book-location.html')

@app.route('/request-hold')
def hold_request():
	return render_template('request-hold.html')

@app.route('/book-checkout')
def book_checkout():
	return render_template('book-checkout.html')

@app.route('/return-book')
def return_book_screen():
	return render_template('return-book-screen.html')

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


@app.route('/damaged-books-report')
def damaged_books_report():
	return render_template('damaged-books-report.html')
	
if __name__ == '__main__':
	app.run(debug=True)