from app import db
from models import User

# Empty and Create all tables
db.drop_all()
db.create_all()

test_user1 = User.register(username = "test_user1",
                           password = "password1",
                           email = "test1@test.com",
                           first_name = "first",
                           last_name = "last")

test_user2 = User.register(username = "test_user2",
                           password = "password2",
                           email = "test2@test.com",
                           first_name = "FIRSTNAME",
                           last_name = "LASTNAME")

db.session.add_all([test_user1, test_user2])
db.session.commit()