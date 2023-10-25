import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from datetime import date
from App.controllers import ( 
	create_course,
	get_course,
	assign_course_lecturer,
	get_lecturer_courses,
	get_student_courses,
	get_enrolled_students,
	get_all_courses,
	get_all_courses_json,
	create_review,
	get_review,
	get_all_reviews,
	get_all_reviews_json,
	get_student_reviews,
	get_lecturer_reviews,
	create_student,
	update_student_name,
	update_student_year,
	get_student,
	get_student_by_name,
	get_all_students,
	get_all_students_json,
	upvote_student,
	downvote_student,
	assign_course_student,
	create_user,
	get_user,
	# get_user_by_username,
	get_all_users,
	get_all_users_json,
	update_user,
	is_admin,
		
	)

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)
'''
Initialization

'''
@app.cli.command("init", help="Creates and initializes the database in testing mode")
def test_initialize():
	db.drop_all()
	db.create_all()
	print('database intialized')
# This command creates and initializes the database
@app.cli.command("devinit", help="Creates and initializes the database in development mode")
def dev_initialize():
	db.drop_all()
	db.create_all()
	# creating admin type users
	roxa_admin = create_user('Roxa','adminroxa','roxa01','Admin')
	marc_admin = create_user('Marc','adminmarc','marc02','Admin')
	
	# creating lecturer type users
	simon_lecturer = create_user('Simon','simonl','simonx1','Lecturer')
	liam_lectuter = create_user('Liam','liaml','liamx2','Lecturer')
	kari_lecturer = create_user('Kari','karil','karix3','Lecturer')

	# creating students
	faith_student = create_student('Faith',3)
	matthew_student = create_student('Matthew',2)
	jarrod_student = create_student('Jarrod',2)
	naomi_student = create_student('Naomi',1)

	# creating courses
	comp01 = create_course('COMP01','Intro to Computer Science')
	comp02 = create_course('COMP02','Intro to Programming')
	comp03 = create_course('COMP03','Programming 2')
	comp04 = create_course('COMP04','Programming 3')
	comp05 = create_course('COMP05','Data Structures')
	info01 = create_course('INFO01','Intro to WWW')
	info02 = create_course('INFO02','Networking')
	inf003 = create_course('INFO03','Web Programming')
	math01 = create_course('MATH01','Mathematics for Computing')
	math02 = create_course('MATH02','Intro to Statistics')
	print('developer database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("name", default="jane")
@click.argument("username", default="defuser")
@click.argument("password", default="defpass")
@click.argument("user_type", default="Lecturer")
def create_user_command( name, username, password, user_type):
	create_user(name, username, password, user_type)
	print(f'user {username} created!')

# this command will be : flask user create bob bobpass
@user_cli.command("get", help='gets a user')
# @click.argument("method", default="id")
@click.argument("searchval", default=1)
def get_user_command(searchval):
	id = searchval
	print(get_user(id))

@user_cli.command("list", help="Lists users in the database")
@click.argument("method", default="string")
def list_user_command(method):
	if method == 'string':
		print(get_all_users())
	else:
		print(get_all_users_json())

@user_cli.command("update", help="Updates user's username")
@click.argument("id", default=1)
@click.argument("username", default="newdef")
def update_user_command(id,username):
	print(update_user(id,username))

@user_cli.command("admin", help="Determines if a user is an Admin")
@click.argument("id", default=1)
def determine_if_admin_command(id):
	print(is_admin(id))

app.cli.add_command(user_cli) # add the group to the cli


'''
Course Commands
'''
course_cli = AppGroup('course', help='course object commands') 
@course_cli.command("create", help="creates a course")
@click.argument("course_code")
@click.argument("course_name")
def create_course_command(course_code,course_name):
	create_course(course_code, course_name)
	print(f'course {course_code} created!')

@course_cli.command("get", help="gets a course based on input (id, lecturer id, student id)")
@click.argument("method", default="id")
@click.argument("searchval", default=1)
def get_course_command(method, searchval):
	if method == 'id':
		id = searchval
		print(get_course(id))
	elif method == 'lecturer':
		lecturer_id = searchval
		print(get_lecturer_courses(lecturer_id))
	elif method == 'student':
		student_id = searchval
		print(get_student_courses(student_id))
	elif method == 'enrolled':
		id = searchval
		print(get_enrolled_students(id))

@course_cli.command("list", help="Lists courses in the database")
@click.argument("method", default="string")
def list_course_command(method):
	if method == 'string':
		print(get_all_courses())
	else:
		print(get_all_courses_json())

@course_cli.command("assign", help="assigns person (lecturer or student) to course")
@click.argument("course_id", default=1)
@click.argument("person_id", default=1)
@click.argument("method", default="lecturer")
def assign_course_student_command(course_id,person_id,method):
	if method == "lecturer":
		print(assign_course_lecturer(course_id,person_id))
	else:
		print(assign_course_student(course_id,person_id))
# @course_cli.command("assign", help="assigns lecturer to course")
# @click.argument("course_id", default=1)
# @click.argument("lecturer_id", default=1)
# def assign_course_lecturer_command(course_id, lecturer_id):
# 	print(assign_course_lecturer(course_id,lecturer_id))



app.cli.add_command(course_cli) # add the group to the cli

'''
Review Commands
'''
review_cli = AppGroup('review', help='review object commands') 
@review_cli.command("create", help="creates a review")
@click.argument("lecturer_id",default = 1)
@click.argument("student_id", default = 1)
@click.argument("comment", default="this is a test comment")
def create_review_command(lecturer_id, student_id, comment):
	create_review(lecturer_id, student_id, comment)
	print(f'review for {student_id} created by {lecturer_id}!')

@review_cli.command("list", help="Lists reviews in the database")
@click.argument("method", default="string")
def list_review_command(method):
	if method == 'string':
		print(get_all_reviews())
	else:
		print(get_all_reviews_json())

@review_cli.command("get", help="gets reviews")
@click.argument("method", default="id")
@click.argument("searchval", default=1)
def get_reviews_command(method, searchval):
	if method == 'id':
		id = searchval
		print(get_review(id))
	elif method == 'lecturer':
		lecturer_id = searchval
		# print(get_lecturer_reviews(lecturer_id))
		print([review.toJSON() for review in get_lecturer_reviews(lecturer_id)])
	elif method == 'student':
		student_id = searchval
		# print(get_student_reviews(student_id))
		print([review.toJSON() for review in get_student_reviews(student_id)])

app.cli.add_command(review_cli) # add the group to the cli

'''
Student Commands
'''
student_cli = AppGroup('student', help='student object commands') 
@student_cli.command("create", help='creates a student')
@click.argument("name",default='John')
@click.argument("year",default=1)
def create_student_command(name,year):
	create_student(name,year)
	print(f'student {name} created')

@student_cli.command("update", help='updates info of a student')
@click.argument("method",default='name')
@click.argument("id",default=1)
@click.argument("inputval",default='newname')
def update_student_command(method,id,inputval):
	if method == "name":
		print(update_student_name(id,inputval))
	else:
		print(update_student_year(id,inputval))

@student_cli.command("get", help='gets a student')
@click.argument("method",default='id')
@click.argument("searchval")
def get_student_command(method,searchval):
	if method == 'id':
		id = searchval
		print(get_student(id))
	else:
		name = searchval
		print(get_student_by_name(name))

@student_cli.command("list", help='Lists students in the database')
@click.argument("method", default="string")
def list_student_command(method):
	if method == 'string':
		print(get_all_students())
	else:
		print(get_all_students_json())

@student_cli.command("karma", help="Add or Remove student karma")
@click.argument("method", default="upvote")
@click.argument("id", default=1)
def modify_student_karma_command(method,id):
	if method == "upvote":
		print(upvote_student(id))
	else:
		print(downvote_student(id))

# @student_cli.command("assign", help="assigns person (lecturer or student) to course")
# @click.argument("course_id", default=1)
# @click.argument("person_id", default=1)
# @click.argument("method", default="lecturer")
# def assign_course_student_command(course_id,person_id,method):
# 	if method == "lecturer":
# 		print(assign_course_lecturer(course_id,person_id))
# 	else:
# 		print(assign_course_student(course_id,person_id))		


app.cli.add_command(student_cli) # add the group to the cli


'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
	if type == "unit":
		sys.exit(pytest.main(["-k", "UserUnitTests"]))
	elif type == "int":
		sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
	else:
		sys.exit(pytest.main(["-k", "App"]))
	

app.cli.add_command(test)