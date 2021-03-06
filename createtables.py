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

def populate_tables():
    populate_users()
    populate_books()

def populate_floors():
    for i in range(1,4):
        query = "INSERT INTO floor VALUES(%s,5,5)"
        values = (i,)
        cursor.execute(query,values)

    for j in range(1,21):

        if j <= 10:
            k = 1
        elif j <= 15:
            k = 2
        elif j <= 20:
            k = 3

        query = "INSERT INTO shelf VALUES(%s,%s,%s)"
        values = (j,j,k)
        cursor.execute(query,values)

    query = "INSERT INTO located_on VALUES(%s,%s)"
    values = [(1001, 1), (1002,1), (1003, 1), (1004, 1), (1005, 11), (1006, 11), (1007, 11), (1008, 16), 
    (1009, 16), (1010, 16), (1011, 16), (1012, 2), (1013, 2), (1014, 2), (1015, 2)]
    for value in values:
        cursor.execute(query,value)
    cnx.commit() 



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

        if(i < 3):
            username = "DEBARRED_STUDENT"+str(i)
            query = "INSERT INTO user VALUES(%s,%s,0)"
            values = (username,password)
            cursor.execute(query,values)

            query = "INSERT INTO student_faculty VALUES(%s,%s,%s,%s,1,%s,%s,0,100,%s)"
            values = (username,username,DOB,"Male",username+"@gatech.edu",username+"land","Computer Science")
            cursor.execute(query,values)


            username = "STAFF"+str(i)
            query = "INSERT INTO user VALUES(%s,%s,1)"
            values = (username,password)
            cursor.execute(query,values)

            query = "INSERT INTO student_faculty VALUES(%s,%s,%s,%s,0,%s,%s,0,0,%s)"
            values = (username,username,DOB,"Male",username+"@gatech.edu",username+"land","Computer Science")
            cursor.execute(query,values)

    cnx.commit()    

def populate_books():
    
    subjectDict = {'Computer Science':200,'English':3,'ECE':4,'Math':20,'Biology':1,'Physics':2}
    for subject in subjectDict:
        query = "INSERT INTO subject VALUES(%s,%s)"
        values = (subject,subjectDict[subject])
        cursor.execute(query,values)
    
    isbn_base = 1000
    for i in range(1,16):

        if i < 5: subject = "ECE"
        elif i < 8: subject = "English"
        elif i < 12: subject = "Biology"
        elif i < 16: subject = "Math"

        query = "INSERT INTO book VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        if i <= 3:
            values = (isbn_base+i,"ReservedBook"+str(i),1,1,"Publisher_ReservedBook"+str(i),
                "Place_ReservedBook"+str(i),1,"Computer Science",1000)
            cursor.execute(query,values)

            query = "INSERT INTO author VALUES(%s,%s)"
            values = ("AUTHOR_"+str(isbn_base+i)+"_1",isbn_base+i)
            cursor.execute(query,values)
            values=("AUTHOR_"+str(isbn_base+i)+"_2",isbn_base+i)
            cursor.execute(query,values)


            
        if i > 3:
            values = (isbn_base+i,"Book"+str(i),0,1,"Publisher_Book"+str(i),
                "Place_Book"+str(i),1,subject,1500)
            cursor.execute(query,values)

            query = "INSERT INTO author VALUES(%s,%s)"
            values = ("AUTHOR_"+str(isbn_base+i)+"_1",isbn_base+i)
            cursor.execute(query,values)

        '''
        4.There should be at least 10 books in the library. 3 books with 3 copies, 3 with 7 copies, 
        2 books with 2 copies each, 1 book with 1 copy, and 1 book with 4 copies. 
        '''
        #### GENERATE BOOK COPIES ####
        if i <= 3:
            query = "INSERT INTO book_copy(Is_damaged,Is_checked_out,Is_on_hold,Copy_number,Isbn) VALUES(%s,%s,%s,%s,%s)"
            values = [(1,0,0,1,isbn_base+i),(0,0,0,2,isbn_base+i),(0,0,0,3,isbn_base+i)]
            for value in values:
                cursor.execute(query,value)
        elif i <= 6:
            query = "INSERT INTO book_copy(Is_damaged,Is_checked_out,Is_on_hold,Copy_number,Isbn) VALUES(%s,%s,%s,%s,%s)"
            values = [(1,0,0,1,isbn_base+i),(0,0,0,2,isbn_base+i),(0,0,0,3,isbn_base+i),(0,0,0,4,isbn_base+i),(0,0,0,5,isbn_base+i)
            ,(0,0,0,6,isbn_base+i),(0,0,0,7,isbn_base+i)]
            for value in values:
                cursor.execute(query,value)
        elif i <= 8:
            query = "INSERT INTO book_copy(Is_damaged,Is_checked_out,Is_on_hold,Copy_number,Isbn) VALUES(%s,%s,%s,%s,%s)"
            values = [(1,0,0,1,isbn_base+i),(0,0,0,2,isbn_base+i)]
            for value in values:
                cursor.execute(query,value)
        elif i <= 14:
            query = "INSERT INTO book_copy(Is_damaged,Is_checked_out,Is_on_hold,Copy_number,Isbn) VALUES(%s,%s,%s,%s,%s)"
            value = (1,0,0,1,isbn_base+i)
            cursor.execute(query,value)

        else:
            query = "INSERT INTO book_copy(Is_damaged,Is_checked_out,Is_on_hold,Copy_number,Isbn) VALUES(%s,%s,%s,%s,%s)"
            values = [(1,0,0,1,isbn_base+i),(0,0,0,2,isbn_base+i),(0,0,0,3,isbn_base+i),(0,0,0,4,isbn_base+i)]
            for value in values:
                cursor.execute(query,value)
 
    cnx.commit()




#drop_tables()
#create_tables()
#populate_users()
#populate_books()
populate_floors()

cursor.close()
cnx.close()
