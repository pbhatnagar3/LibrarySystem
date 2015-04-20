from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'libpro'

TABLES = {}

TABLES['user'] = (
    "CREATE TABLE `user` ("
    "  `Username` varchar(50) NOT NULL,"
    "  `Password` varchar(50) NOT NULL,"
    "  PRIMARY KEY (`Username`)"
    ") ENGINE=InnoDB")

TABLES['staff'] = (
	"CREATE TABLE `staff` ("
    "  `Username` varchar(50) NOT NULL,"
    "  PRIMARY KEY (`Username`),"
    "  FOREIGN KEY (`Username`) REFERENCES user (`Username`)"
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
    "  `Date_of_issue` DATE NOT NULL,"
    "  `Extension_date` DATE NOT NULL,"
    "  `Return_date` DATE NOT NULL,"
    "  `Count_of_extensions` SMALLINT NOT NULL,"
    "  `Copy_id` INT NOT NULL,"
    "  `Isbn` VARCHAR(50) NOT NULL,"
    "  PRIMARY KEY (`Issue_id`),"
    "  FOREIGN KEY (`Copy_id`) REFERENCES book_copy (`Copy_number`),"
    "  FOREIGN KEY (`Isbn`) REFERENCES book_copy (`Isbn`)"
    ") ENGINE=InnoDB")

TABLES['book_copy'] = (
	"CREATE TABLE `book_copy` ("
    "  `Future_requester` varchar(50) NOT NULL,"
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
    "  `Isbn` varchar(50) NOT NULL,"
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

cnx = mysql.connector.connect(user='group62', 
		password='_password', 
		host="cs4400-library-management.c0erkhridnqw.us-east-1.rds.amazonaws.com", 
		database="libpro")
cursor = cnx.cursor()


# DROP EXISTING TABLES
for name, ddl in TABLES.iteritems():
	try:
		print("Dropping table {}: ".format(name), end='')
		cursor.execute("DROP TABLE " + name)
	except mysql.connector.Error as err:
		print(err.msg)
	else:
		print("OK")

# CREATE TABLES
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

cursor.close()
cnx.close()
