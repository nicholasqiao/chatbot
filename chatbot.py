import sqlite3
from sqlite3 import Error

def cli():
	db_file = "database.db"
	
	try:
		conn = sqlite3.connect(db_file)
	except Error as e:
		print (e)

	cursor = conn.cursor()

	choice = 0
	while choice < 5:
		print "+===========+"
		print "| MAIN MENU |"
		print "+===========+"
		print "1) Insert new question text to database"
		print "2) Modify Exising question"
		print "3) Read and display diff of changes to question text over time"
		print "4) Input User Response"
		print "5) Exit"
		choice = input ("Selection: ")
		
		if choice == 1:
			insertQuestion(cursor, conn)
		elif choice == 2:
			modifyQuestion(cursor, conn)
		elif choice == 3:
			displayDiff(cursor, conn)
		elif choice == 4:
			userResponse(cursor, conn)

def insertQuestion(cursor, conn):
	print "+=====================+"
	print "| INSERT NEW QUESTION |"
	print "+=====================+"

	question_text = raw_input ("New Question: ")
	question_topic = raw_input ("Question Topic: ")

	#Add new question into questions table
	query = "INSERT INTO questions values (NULL, ?,1)"
	cursor.execute(query, (question_topic,))

	#Getting current questionID to use to add to changes table
	question_id = cursor.lastrowid

	#Add new question into changes table
	query = "INSERT INTO changes values (?,?,?)" 
	cursor.execute(query, (question_id, 1, question_text))
	conn.commit()		

def modifyQuestion(cursor, conn):
	print "+==========================+"
	print "| MODIFY EXISTING QUESTION |"
	print "+==========================+"

	question_id = input ("Question ID: ")

	query = "SELECT MAX(questionID) FROM questions"
	res = cursor.execute(query).fetchall()
	maxID = res[0][0]
	
	if question_id <= maxID:
		question_text = raw_input ("New Question: ")

		#Find max iteration
		query = "SELECT MAX(iterID) FROM changes WHERE questionID = ?"		
		res = cursor.execute(query, (question_id,))
		reslist = res.fetchall()
		iter_id = reslist[0][0]

		#Update changes Table
		query = "INSERT INTO changes values (?,?,?)" 
		cursor.execute(query, (question_id, iter_id+1, question_text))
		conn.commit()

		#Update questions Table (to get text from changes table)
		query = "UPDATE questions SET iterID = ? where questionID = ?"
		cursor.execute(query, (iter_id+1, question_id))
		conn.commit()
	else:
		print "Question ID Does Not Exist"


def displayDiff(cursor, conn):
	print "+==========================+"
	print "| DISPLAY QUESTION HISTORY |"
	print "+==========================+"

	question_id = input ("Question ID: ")
	query = "SELECT iterID,text FROM changes where questionID = ?"
	res = cursor.execute(query, (question_id,)).fetchall()

	if len(res) == 0:
		print "No records found..."
	else:
		for x in res:
			print x[0], x[1]

def userResponse(cursor, conn):
	print "+=====================+"
	print "| INPUT USER RESPONSE |"
	print "+=====================+"

	user_id = input ("User ID: ")
	question_id = input ("Responding to Question ID: ")
	iter_id = input ("# Iteration of Question: ")
	response_text = raw_input ("Response: ")

	query = "INSERT INTO user_responses values (?, ?, ?, ?)"

	# question_id, iter_id, user_id should be filled in 
	# based off what question is being answered
	cursor.execute(query, (question_id, iter_id, user_id, response_text))
	conn.commit()

if __name__ == "__main__":
	cli()
