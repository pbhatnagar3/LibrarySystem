#5 Request Hold on Book

# When the submit button is clicked, select the lowest copy_number available of the selected ISBN
SELECT MIN(Copy_number) FROM book_copy WHERE Isbn = $ISBN AND Is_checked_out = 0 AND Is_on_hold = 0
# Once we select that MIN(Copy_number), we need to set that copy_number to be on Is_on_hold
UPDATE book_copy SET Is_on_hold = 1 WHERE Isbn = $ISBN AND Copy_number = $MIN_COPY_NUMBER
# We also need to create an issue. No need to insert Issue_id as Issue_id is auto-incremented
INSERT INTO issue (Date_of_issue,Extension_date,Return_date,Count_of_extensions,Copy_id,Isbn) VALUES($Current_Date,$Current_Date + 17,$Current_Date + 17,0,$Copy_Id,$ISBN)
#----------------------------------------------------------------------------------------------
#6 Request Extension for an Issued Book

# User can request an extension for CHECKED_OUT BOOKS ONLY by giving the Issue_id
SELECT * FROM issue WHERE Issue_id = $Issue_id # (1)
# This returns (Date_of_Issue, Extension_date,Return_date,Count_of_extensions,Copy_id,Isbn)
# WE NEED Username to identify whether the user is faculty or not
SELECT Is_faculty FROM student_faculty WHERE Username = $Username # (2)

#Also we need to check whether the particular Isbn and Copy_number is CHECKED_OUT (Can only request extension if it's checked out)
SELECT Is_checked_out FROM book_copy WHERE Isbn = $ISBN and Copy_number = $Copy_id

'''
allowExtension = False

if (Is_checked_out): 
	On the Request extenion on book page, there are fields that we need to fill in
	1) Original Checkout Date = Date_of_Issue from (1)
	2) Current Extension Date = Extension_date from (1)
	3) Current Return Date = Return_date from (1)

	if(Is_faculty and (($Current_Date + 14 - Date_of_Issue) <= 56) and (Count_of_extensions < 5): #FACULTY CASE
		4) New Extension Date = $Current_date 
		5) New Estimated Return Date = $Current_date + 14
		allowExtension = True
		
	elif ((Is_faculty == 0) and (($Current_Date + 14 - Date_of_Issue) <= 28) and (Count_of_extensions < 2)): #STUDENT CASE 
		4) New Extension Date = $Current_date 
		5) New Estimated Return Date = $Current_date + 14
		allowExtension = True 

	else:
		4) New Extension Date = "Unable to grant extension"
		5) New Estimated Return Date = "Unable to grant extension"
else:
	Set all fields to "Book is not checked out"

'''
# IF SUBMIT_BUTTON is clicked
If(allowExtension):
	UPDATE issue SET Extension_date = $Current_date,Return_date = $Current_date + 14, Count_of_extensions = $Count_of_extensions+1 
	WHERE Issue_id = $Issue_id

else:
	"Notification that an extension cannot be granted for this Issue_id"

#----------------------------------------------------------------------------------------------
#7 Future Hold Request for a Book

# User provides ISBN of the book he wishes to request a hold, and the system looks for the book_copy that will be available soonest
# AGAIN WE NEED $Username possibly from the sign in page

# Find the copy_number of ISBN that is checked out
SELECT Copy_number,Is_damaged FROM book_copy WHERE Is_checked_out = 1 AND Isbn = $ISBN

copyNo_to_returnDate = dict()

for copy_number in Copy_number:
	SELECT Return_date FROM issue WHERE Isbn = $ISBN AND Copy_id = copy_number
	copyNo_to_returnDate[copy_number] = Return_date

'''
On the screen, the program will show two fields
1) Copy Number = min(copyNo_to_returnDate,key=copyNo_to_returnDate.get)
2) Expected available date = copyNo_to_returnDate[min(copyNo_to_returnDate,key=copyNo_to_returnDate.get)]  
'''

# When OK button is clicked
INSERT INTO book_copy VALUES($Username,$Is_damaged,0,1,$Copy_number,$Isbn)

#----------------------------------------------------------------------------------------------
#8 Track Location 

# User enters ISBN and clicks "Locate". The program will show Floor Number, Shelf Number, Aisle Number, and Subject
SELECT Shelf_number FROM located_on WHERE Isbn = $ISBN
# Once we know the Shelf_number
SELECT Aisle_number,Floor_number FROM shelf WHERE Shelf_number = $Shelf_number
# Find Subject name
SELECT Subject_name FROM book WHERE Isbn = $ISBN

'''
Output the following
1) Floor Number
2) Aisle Number
3) Shelf Number
4) Subject



