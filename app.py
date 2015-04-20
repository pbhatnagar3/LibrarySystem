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
def createProfile():
	return render_template('create-profile.html')



	
if __name__ == '__main__':
	app.run(debug=True)