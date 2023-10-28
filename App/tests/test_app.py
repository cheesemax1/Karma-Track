import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from App.main import create_app
from App.database import db, create_db
from App.models import User,Student,Course,Review
from App.controllers import (
    login,
    create_admin,
    create_lecturer,
    get_all_users_json,
    get_user,
    get_user_by_username,
    update_user_name,
    update_user_type,
    create_student,
    get_student,
    get_student_by_name,
    update_student_name,
    update_student_year,
    get_all_students_json,
    upvote_student,
    downvote_student,
    create_review,
    get_review,
    get_all_reviews_json,
    get_student_reviews,
    get_lecturer_reviews,
    create_course,
    get_course,
    assign_course_lecturer,
    assign_course_student,
    get_lecturer_courses,
    get_enrolled_students
)
unittest.TestLoader.sortTestMethodsUsing = None

LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("testname" , "tester1", "testpass" , "Lecturer")
        error_msg = f"testname expected, got: {user.name}\n\
            Lecturer expected, got: {user.user_type}"
        assert user.name == "testname"

    def test_password_is_hashed(self):
        password = "testpass"
        user = User("testname" , "a1test", password, "Admin")
        error_msg = "password is not hashed, function returns string"
        assert user.password != password

    def test_check_password(self):
        password = "testpass"
        user = User("testname" , "a1test", password, "Admin")
        assert user.check_password(password)

    def test_user_is_admin(self):
        user = User("admintest" , "atest", "testpass", "Admin")
        assert user.is_admin()

    def test_change_user_name(self):
        user = User("testname" , "l1test", "testpass" , "Lecturer")
        user.set_name("unittestname")
        assert user.name == "unittestname"

    def test_change_user_type(self):
        user = User("testname" , "l1test", "testpass" , "Lecturer")
        user.set_user_type("Admin")
        assert user.user_type == "Admin"
        
    def test_add_review(self):
        review = Review(1,1,"user unit test comment")
        user = User("testname" , "l1test", "testpass" , "Lecturer")
        user.add_review(review)
        assert review in user.reviews
    
    def test_add_course(self):
        course = Course("UTest01","User Unit Test Course")
        user = User("testname" , "l1test", "testpass" , "Lecturer")
        user.add_course(course)
        assert course in user.courses 

    def test_get_json(self):
        user = User("testname" , "l1test", "testpass" , "Lecturer")
        user_json = user.to_json()
        self.assertDictEqual(
            user_json, {
                "id":None, 
                "name":"testname",
                "username" : "l1test",
                "type" : "Lecturer",
                "courses" : [],
                "reviews" : []
                })
class StudentUnitTests(unittest.TestCase):
    def test_new_student(self):
        student = Student("Walter", 3)
        assert student.name == "Walter"
    
    def test_change_student_name(self):
        student = Student("Walter", 3)
        student.set_name("newstudent")
        assert student.name == "newstudent"
    def test_change_student_year(self):
        student = Student("Walter", 3)
        student.set_year(4)
        assert student.year == 4

    def test_upvote_student(self):
        student = Student("Walter", 3)
        student.modify_karma("+")
        assert student.karma == 1

    def test_downvote_student(self):
        student = Student("Walter", 3)
        student.modify_karma("-")
        assert student.karma == -1

    def test_student_to_json(self):
        student = Student("Ayre", 6)
        self.assertDictEqual(student.to_json(),{
            "id":None, 
            "name":"Ayre", 
            "year":6, 
            "karma":0, 
            "courses":[], 
            "reviews":[]
        })
class CourseUnitTests(unittest.TestCase):
    def test_new_course(self):
        course = Course("COMP3613","Software 2")
        assert course.course_code == "COMP3613"
    def test_assign_course_lecturer(self):
        course = Course("COMP3613","Software 2")
        course.assign_lecturer(1)
        assert course.lecturer_id == 1

    def test_course_to_json(self):
        course = Course("COMP3602","Theory of Computing")
        self.assertDictEqual(course.to_json(),{
            "id" : None,
            "lecturer" : None,
            "course_code" : "COMP3602",
            "course_name" : "Theory of Computing"
        })
class ReviewUnitTests(unittest.TestCase):
    def test_new_review(self):
        review = Review(1,1,"unit test comment")
        assert review.comment == "unit test comment"

    def test_review_to_json(self):
        review = Review(1,1,"another comment")
        rn = datetime.utcnow().strftime('%d-%m-%Y')
        self.assertDictEqual(review.to_json(),{
            "review_id":None, 
            "lecturer": 1, 
            "student": 1, 
            "review_date": rn ,
            "comment" : "another comment"
        })

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.session.remove()
    db.drop_all()

#NOTE: Integration test class can only see what is inside its scope, when run alone, and beyond it when running all tests
class UserIntegrationTests(unittest.TestCase):
    def test_create_user(self):
            mark = create_admin("mark" ,"test01", "pass01")
            user = get_user(mark.id)
            assert user.username == mark.username


    def test_is_admin_user(self):
        user = get_user(1)
        assert user.is_admin()

    def test_get_all_users_json(self):
        create_lecturer("felix", "nextup", "rnd03")
        users_json = get_all_users_json()
        self.assertListEqual(
            users_json,
            [
                {
                    "id":1, 
                    "name" : 'mark',
                    "username":"test01",
                    "type" : "Admin",
                    "courses" : [],
                    "reviews" : [],
                },
                {
                    "id":2, 
                    "name" : 'felix',
                    "username":"nextup",
                    "type" : "Lecturer",
                    "courses" : [],
                    "reviews" : [],
                },
            ]
        )

    # Tests data changes in the database
    def test_update_user_name(self):
        update_user_name(1,"newtestname")
        user = get_user(1)
        assert user.name == "newtestname"
    def test_update_user_type(self):
        update_user_type(2,"Admin")
        user = get_user(2)
        assert user.user_type == "Admin"

#NOTE: DEPENDING ON THE NAME OF THE FUNCTION, RESULTS MAY CHANGE AS THE ORDER OF EXECUTION CHANGES
class StudentIntegrationTests(unittest.TestCase):
    def test_create_student(self):
        create_student("Bea", 2)
        student = get_student(1)
        assert student.name == "Bea"

    def test_update_student_name(self):
        update_student_name(1,"Beatrice")
        student = get_student(1)
        assert student.name == "Beatrice"

    def test_update_student_year(self):
        update_student_year(1,3)
        student = get_student(1)
        assert student.year == 3

    def test_zget_all_students_json(self):
        students_json = get_all_students_json()
        self.assertListEqual(
            students_json,
            [
                {
                    "id":1, 
                    "name":"Beatrice", 
                    "year":3, 
                    "karma":1, 
                    "courses":[], 
                    "reviews":[]
                },
                {
                    "id":2, 
                    "name":"Raine", 
                    "year":5, 
                    "karma":-1, 
                    "courses":[], 
                    "reviews":[]
                }
            ]
        )

    def test_upvote_student(self):
        bea = upvote_student(1)
        student = get_student(1)
        assert bea.karma == student.karma


    def test_downvote_student(self):
        create_student("Raine", 5)
        raine = downvote_student(2)
        student = get_student(2)
        assert raine.karma == student.karma

class CourseIntegrationTests(unittest.TestCase):
    
    def test_create_course(self):
        course = create_course("COMP3603","HCI")
        assert get_course(course.course_id).course_code == "COMP3603"

    def test_assign_course_lecturer(self):
        l1 = create_lecturer("Mili","Milily","cour01")
        course = create_course("COMP3605","Data Analytics")
        assigned_course = assign_course_lecturer(course.course_id,l1.id)
        assert assigned_course.lecturer_id == l1.id
    def test_assign_course_student(self):
        s1 = create_student("Naomi",3)
        course = create_course("COMP3607","OOP2")
        assigned_course = assign_course_student(course.course_id,s1.id)
        self.assertIn(course,s1.courses)

class AuthIntegrationTests(unittest.TestCase):
    def test_login(self):
            user = create_lecturer("logintest" ,"logger01","logpass")
            assert login("logger01", "logpass") != None

class ReviewIntegrationTests(unittest.TestCase):
    def test_create_review(self):
        l1 = create_lecturer("reviewer", "rev01","revpass")
        s1 = create_student("reviewee",1)
        review = create_review(l1.id,s1.id,"integration review comment")
        assert get_review(1).comment == "integration review comment" and review in get_user(l1.id).reviews and review in get_student(s1.id).reviews
    
    def test_get_reviews_student(self):
        s1 = get_student_by_name("reviewee")
        l2 = create_lecturer("reviewer2", "rev02","revpass2")
        review = create_review(l2.id,s1.id,"integration test get student's reviews")
        student_reviews = get_student_reviews(s1.id)
        self.assertListEqual(student_reviews,[get_review(1),get_review(2)])

    def test_get_reviews_zlecturer(self):
        lecturer = get_user_by_username("rev01")
        s2 = create_student("reviewee2",2)
        review = create_review(lecturer.id,s2.id,"integration test get lecturer's reviews")
        lect_reviews = get_lecturer_reviews(lecturer.id)
        self.assertListEqual(lect_reviews,[get_review(1),get_review(3)])


    

