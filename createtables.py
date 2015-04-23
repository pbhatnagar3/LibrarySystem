from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'libpro'

TABLES = {}

TABLES['user'] = (
    "CREATE TABLE `user` ("
    "  `Username` varchar(50) NOT NULL,"
    "  `Password` varchar(50) NOT NULL,"
    "  `Is_staff` BOOLEAN DEFAULT 0,"
    "  PRIMARY KEY (`Username`)"
    ") ENGINE=InnoDB")

TABLES['student_faculty'] = (
	"CREATE TABLE `student_faculty` ("
    "  `Username` varchar(50) NOT NULL,"
    "  `Name` varchar(100) NOT NULL,"
    "  `Dob` DATE,"
    "  `Gender` varchar(6),"
    "  `Is_debarred` BOOLEAN NOT NULL,"
    "  `Email` varchar(50) NOT NULL,"
    "  `Address` varchar(250),"
    "  `Is_faculty` BOOLEAN NOT NULL,"
    "  `Penalty` SMALLINT NOT NULL,"
    "  `Department` varchar(100),"
    "  PRIMARY KEY (`Username`),"
    "  FOREIGN KEY (`Username`) REFERENCES user (`Username`)"
    ") ENGINE=InnoDB"
	)

TABLES['issue'] = (
	"CREATE TABLE `issue` ("
    "  `Issue_id` INTEGER AUTO_INCREMENT,"
    "  `Username` varchar(50) NOT NULL,"
    "  `Date_of_issue` DATE NOT NULL,"
    "  `Extension_date` DATE NOT NULL,"
    "  `Return_date` DATE NOT NULL,"
    "  `Count_of_extensions` SMALLINT NOT NULL,"
    "  `Copy_id` INT NOT NULL,"
    "  `Isbn` VARCHAR(50) NOT NULL,"
    "  PRIMARY KEY (`Issue_id`),"
    "  FOREIGN KEY (`Username`) REFERENCES user (`Username`),"
    "  FOREIGN KEY (`Copy_id`) REFERENCES book_copy (`Copy_number`),"
    "  FOREIGN KEY (`Isbn`) REFERENCES book_copy (`Isbn`)"
    ") ENGINE=InnoDB")

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

TABLES['author'] = (
	"CREATE TABLE `author` ("
    "  `Name` varchar(50),"
    "  `Isbn` varchar(50),"
    "  PRIMARY KEY (`Name`, `Isbn`),"
    "  FOREIGN KEY (`Isbn`) REFERENCES book (`Isbn`)"
    ") ENGINE=InnoDB")

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

TABLES['subject'] = (
	"CREATE TABLE `subject` ("
    "  `Name` varchar(50),"
    "  `Number_of_journals` INT,"
    "  PRIMARY KEY (`Name`)"
    ") ENGINE=InnoDB")

TABLES['located_on'] = (
	"CREATE TABLE `located_on` ("
    "  `Isbn` varchar(50) NOT NULL,"
    "  `Shelf_number` INT,"
    "  PRIMARY KEY (`Isbn`, `Shelf_number`),"
    "  FOREIGN KEY (`Isbn`) REFERENCES book (`Isbn`),"
    "  FOREIGN KEY (`Shelf_number`) REFERENCES shelf (`Shelf_number`)"
    ") ENGINE=InnoDB")

TABLES['shelf'] = (
	"CREATE TABLE `shelf` ("
    "  `Shelf_number` INT,"
    "  `Aisle_number` INT,"
    "  `Floor_number` INT NOT NULL,"
    "  PRIMARY KEY (`Shelf_number`),"
    "  FOREIGN KEY (`Floor_number`) REFERENCES floor (`Floor_number`)"
    ") ENGINE=InnoDB")

TABLES['floor'] = (
	"CREATE TABLE `floor` ("
    "  `Floor_number` INT,"
    "  `Number_Student_Assistant` INT,"
    "  `Number_of_Copiers` INT,"
    "  PRIMARY KEY (`Floor_number`)"
    ") ENGINE=InnoDB")


# cnx = mysql.connector.connect(user='group62', 
# 		password='password', 
# 		host="localhost", 
#         port="8889",
# 		database="libpro")
cnx = mysql.connector.connect(user='group62', 
        password='_password', 
        host="cs4400-library-management.c0erkhridnqw.us-east-1.rds.amazonaws.com", 
        database="libpro")
cursor = cnx.cursor()


def drop_tables():
    for name, ddl in TABLES.iteritems():
    	try:
    		print("Dropping table {}: ".format(name), end='')
    		cursor.execute("DROP TABLE " + name)
    	except mysql.connector.Error as err:
    		print(err.msg)
    	else:
    		print("OK")

# CREATE TABLES
def create_tables():
    for name, ddl in TABLES.iteritems():
        try:
            print("Creating table {}: ".format(name), end='')
            cursor.execute(ddl)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

# POPULATE TABLES ACCORDING TO REQUIREMENT
def populate_users():
    specialUser = ['natch','rohit','pujun']
    password = 'password'
    DOB = "1993-08-02"

    for user in specialUser:
        query = "INSERT INTO user VALUES(%s,%s,0)"
        values = (user,password)
        cursor.execute(query,values)

        query = "INSERT INTO student_faculty VALUES(%s,%s,%s,%s,0,%s,%s,0,0,%s)"
        values = (user,user,DOB,"Male",user+"@gatech.edu",user+"land","Computer Science")
        cursor.execute(query,values)    
    
    for i in range(1,16):
        username = "STUDENT"+str(i)
        query = "INSERT INTO user VALUES(%s,%s,0)"
        values = (username,password)
        cursor.execute(query,values)

        query = "INSERT INTO student_faculty VALUES(%s,%s,%s,%s,0,%s,%s,0,0,%s)"
        values = (username,username,DOB,"Male",username+"@gatech.edu",username+"land","Computer Science")
        cursor.execute(query,values)

        if(i < 6):
            query = "INSERT INTO user VALUES(%s,%s,0)"
            username = "FACULTY"+str(i)
            values = (username,password)
            cursor.execute(query,values)

            query = "INSERT INTO student_faculty VALUES(%s,%s,%s,%s,0,%s,%s,1,0,%s)"
            values = (username,username,DOB,"Male",username+"@gatech.edu",username+"land","Computer Science")
            cursor.execute(query,values)

    for i in range(1,3):
        username = "DEBARRED_STUDENT"+str(i)
        query = "INSERT INTO user VALUES(%s,%s,0)"
        values = (username,password)
        cursor.execute(query,values)

        query = "INSERT INTO student_faculty VALUES(%s,%s,%s,%s,1,%s,%s,0,100,%s)"
        values = (username,username,DOB,"Male",username+"@gatech.edu",username+"land","Computer Science")
        cursor.execute(query,values)

    for i in range(1,3):
        username = "STAFF"+str(i)
        query = "INSERT INTO user VALUES(%s,%s,1)"
        values = (username,password)
        cursor.execute(query,values)

        query = "INSERT INTO student_faculty VALUES(%s,%s,%s,%s,0,%s,%s,0,0,%s)"
        values = (username,username,DOB,"Male",username+"@gatech.edu",username+"land","Computer Science")
        cursor.execute(query,values)

    cnx.commit()




#drop_tables()
#create_tables()
populate_users()


cursor.close()
cnx.close()
