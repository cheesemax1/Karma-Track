import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import ( 
    create_user, 
    get_all_users_json, 
    get_all_users, 
    create_course,
    get_all_courses,
    get_lecturer_courses,
    get_student_courses,
    get_student_reviews,
    get_lecturer_reviews
    )

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bob01','bobpass', 'Lecturer')
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="robx2")
@click.argument("password", default="robpass")
@click.argument("name", default="robpass")
@click.argument("user_type", default="Admin")
def create_user_command( name, username, password, user_type):
    create_user(name, username, password, user_type)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass


@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Course Commands
'''
course_cli = AppGroup('course', help='course object commands') 
@course_cli.command("create", help="creates a course")
@click.argument("lecturer_id")
@click.argument("course_code")
@click.argument("course_name")
def create_course_command(lecturer_id, course_code, course_name):
    create_course(lecturer_id, course_code, course_name)
    print(f'course {course_code} created!')

@course_cli.command("list", help="Lists courses in the database")
def list_course_command():
    print(get_all_courses())

@course_cli.command("get-l", help="gets lecturer courses")
@click.argument("lecturer_id")
def get_lecturer_courses_command(lecturer_id):
    print(get_lecturer_courses(lecturer_id))

@course_cli.command("get-s", help="gets student courses")
@click.argument("student_id")
def get_student_courses_command(student_id):
    print(get_student_courses(student_id))


app.cli.add_command(course_cli) # add the group to the cli

'''
Review Commands
'''
review_cli = AppGroup('review', help='review object commands') 
@review_cli.command("create", help="creates a review")
@click.argument("lecturer_id")
@click.argument("student_id")
@click.argument("comment")
def create_review_command(user_id, student_id, comment):
    create_review(user_id, student_id, comment)
    print(f'review for {student_id} created by {lecturer_id}!')

@review_cli.command("list", help="Lists reviews in the database")
def list_review_command():
    print(get_all_reviews())

@review_cli.command("get-l", help="gets lecturer reviews")
@click.argument("lecturer_id")
def get_lecturer_reviews_command(lecturer_id):
    print(get_lecturer_reviews(lecturer_id))

@review_cli.command("get-s", help="gets student reviews")
@click.argument("student_id")
def get_student_reviews_command(student_id):
    print(get_student_reviews(student_id))


app.cli.add_command(course_cli) # add the group to the cli

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