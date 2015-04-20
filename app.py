from flask import Flask, render_template, request
import database

try:
	database.connect()
except Exception, e:
	print "failed" 
else:
	pass
finally:
	pass
	
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

@app.route('/login/', methods=['POST', 'GET'])
def login():
	if request.method == 'POST':
		print request.form['username'], request.form['password']
		# return logged in view
		return 'logged in!'


@app.route('/create-profile')
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


	
if __name__ == '__main__':
	app.run(debug=True)