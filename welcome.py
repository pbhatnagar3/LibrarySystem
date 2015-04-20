from flask import Flask, render_template
import mysql.connector as sql
from mysql.connector import errorcode

cnx = sql.connect(user='group62', 
	password='_password', 
	host="cs4400-library-management.c0erkhridnqw.us-east-1.rds.amazonaws.com", 
	database="libpro")



# cur = db.cursor()
# from sqlalchemy import create_engine, MetaData

# engine = create_engine('sqlite:////tmp/test.db', convert_unicode=True)
# metadata = MetaData(bind=engine)

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
	
if __name__ == '__main__':
	app.run(debug=True)