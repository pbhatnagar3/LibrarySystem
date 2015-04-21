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
