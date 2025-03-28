# -*- coding: utf-8 -*-
"""
    models.py
    ~~~~~~~~~

    Outlines tables stored SQLite database including: User

    :copyright: (c) 2024 by Newcastle University CSC2033 Team 8.
    :license: see LICENSE.MD for more details.
"""
import bcrypt

from flask_login import UserMixin

import datetime

import pyotp
from app import db, app
from generate_test_data import emissions


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    pin_key = db.Column(db.String(32), nullable=False, default=pyotp.random_base32())
    private = db.Column(db.String(1), nullable=False)

    def __init__(self, email, password, firstname, lastname, username, role):
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.role = role
        self.private = "0"  # if private = 1, the account is private. 0 means public

    def verify_username(self, username):
        return self.username == username

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def hash_password(self, new_password):
        return bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    

    def get_2fa_uri(self):
        return str(pyotp.totp.TOTP(self.pin_key).provisioning_uri(
            name=self.username,
            issuer_name="Alder Carbon Tracker"
        ))


class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    activity_type = db.Column(db.String(100), nullable=False)
    car_fuel_type = db.Column(db.String(100), nullable=True)
    flight_distance = db.Column(db.Integer, nullable=True)
    carbon_emission = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __init__(self, user_id, activity_type, carbon_emission, date, fuel_type=None, flight_distance=None):
        self.user_id = user_id
        self.activity_type = activity_type
        self.fuel_type = fuel_type
        self.flight_distance = flight_distance
        self.carbon_emission = carbon_emission
        self.date = date


class Friendships(db.Model):
    __tablename__ = 'friendships'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, user_id, friend_id):
        self.user_id = user_id
        self.friend_id = friend_id


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    date_posted = db.Column(db.DateTime)
    likes_count = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, title, content):
        self.user_id = user_id
        self.title = title
        self.content = content
        self.date_posted = datetime.datetime.now()
        self.likes_count = 0


class Comments(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    content = db.Column(db.String(1000), nullable=False)

    def __init__(self, user_id, post_id, content):
        self.user_id = user_id
        self.post_id = post_id
        self.content = content


class Likes(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id


def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        admin = User(email="admin@email.com",
                     password="Admin1!",
                     firstname="Nicholas",
                     lastname="Day",
                     username="NickDay",
                     role="admin"
                    )
        db.session.add(admin)
        db.session.commit()
        mainUser = User(email="johnsmith@email.com",
                    password="JohnSmith1!",
                    firstname="John",
                    lastname="Smith",
                    username="JohnSmith007",
                    role="admin"
                    )
        db.session.add(mainUser)
        db.session.commit()
        mainUserPost1 = Post(mainUser.id,
                             title="Wow, this website is so good!!",
                             content="Has anyone noticed how amazing this website is?? It's so helpful for tracking your carbon emission history!")
        mainUserPost1.date_posted = datetime.datetime(2024, 5, 10)
        mainUserPost2 = Post(mainUser.id,
                             title="Just signed up for this website!",
                             content="I really hope this website helps me lower my carbon emissions....")
        mainUserPost2.date_posted = datetime.datetime(2024, 5, 5)
        db.session.add(mainUserPost1)
        db.session.add(mainUserPost2)
        db.session.commit()
        car, foods = emissions(mainUser.id)
        for i in car:
            db.session.add(i)
        for i in foods:
            db.session.add(i)
        db.session.commit()
        user1 = User(email="alicethomas@email.com",
                     password="AliceThomas1!",
                     firstname="Alice",
                     lastname="Thomas",
                     username="AliceThomas42",
                     role="user")
        user2 = User(email="joeslater@email.com",
                     password="JoeSlater1!",
                     firstname="Joe",
                     lastname="Slater",
                     username="JoeSlater3",
                     role="user")
        user3 = User(email="hannahreinsch@email.com",
                     password="HannahReinsch1!",
                     firstname="Hannah",
                     lastname="Reinsch",
                     username="HannahReinsch21",
                     role="user")
        user4 = User(email="nyahgreenwood@email.com",
                     password="NyahGreenwood1!",
                     firstname="Nyah",
                     lastname="Greenwood",
                     username="NyahGreenwood18",
                     role="user")
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.add(user4)
        db.session.commit()
        friend1 = Friendships(mainUser.id, user1.id)
        friend2 = Friendships(mainUser.id, user2.id)
        friend3 = Friendships(mainUser.id, user3.id)
        friend4 = Friendships(mainUser.id, user4.id)
        db.session.add(friend1)
        db.session.add(friend2)
        db.session.add(friend3)
        db.session.add(friend4)
        u1post1 = Post(user1.id,
                       title="Holiday Abroad!",
                       content="Hi!!! I recently went on a holiday abroad and instead of flying I took the train!!! A couple of moths ago I flew to Portugal and it HIT my carbon emissions, this makes me feel so much better!")
        u1post1.likes_count = 3
        u1post1.date_posted = datetime.datetime(2024, 5, 30)
        u1post2 = Post(user1.id,
                       title="Any good vegetarian recipes??",
                       content="Please can someone help!! I've been trying to find some good vegetarian recipes that aren't just salads, please someone helppp!")
        u1post2.likes_count = 2
        u1post2.date_posted = datetime.datetime(2024, 5, 29)
        u2post1 = Post(user2.id,
                       title="Bike to work?",
                       content="Does anyone else bike to work?? I drive like 25km to work every day and it's really affecting my carbon emissionsss")
        u2post1.likes_count = 3
        u2post1.date_posted = datetime.datetime(2024, 5, 27)
        u3post1 = Post(user3.id,
                       title="Trip to Portugal!",
                       content="I just got back from portugal with my girlfriend it was GORGEOUS 10/10 would recommend to anyone looking for cute hikes.")
        u3post1.likes_count = 2
        u3post1.date_posted = datetime.datetime(2024, 5, 26)
        u3post2 = Post(user3.id,
                       title="Corn on the cob.",
                       content="Has anyone else had any corn on the cob recently?? I've been absolutely DEMOLISHING it recently, it's just so GOOOODO")
        u3post2.likes_count = 4
        u3post2.date_posted = datetime.datetime(2024, 5, 23)
        u4post1 = Post(user4.id,
                       title="Theres no corn on the cob at the shops!",
                       content="Is it just me or is there no corn on the cob at the shops anymore??? The shelves used to be stocked with the stuff now i cant find any for the life of me.")
        u4post1.likes_count = 3
        u4post1.date_posted = datetime.datetime(2024, 5, 21)
        db.session.add(u1post1)
        db.session.add(u1post2)
        db.session.add(u2post1)
        db.session.add(u3post1)
        db.session.add(u3post2)
        db.session.add(u4post1)
        db.session.commit()

        u1p1comment1 = Comments(user2.id, u1post1.id, "Trains are so much better anyway imo, the views are stunning!!")
        u1p1comment2 = Comments(user1.id, u1post1.id, "I knowwww! all the hills and endless fields, stunning views :)")
        u1p1like1 = Likes(user2.id, u1post1.id)
        u1p1like2 = Likes(user3.id, u1post1.id)
        u1p1like3 = Likes(user4.id, u1post1.id)
        db.session.add(u1p1comment1)
        db.session.add(u1p1comment2)
        db.session.add(u1p1like1)
        db.session.add(u1p1like2)
        db.session.add(u1p1like3)
        db.session.commit()

        u1p2comment1 = Comments(user3.id, u2post1.id, "Have you tried checking out Gordon Ramsay videos?? He has some amazing tutorials.")
        u1p2comment2 = Comments(user2.id, u1post2.id, "My partner took a cooking course on our trip to Portugal, maybe she could give you a couple recipes??")
        u1p2like1 = Likes(user2.id, u1post2.id)
        u1p2like2 = Likes(user3.id, u1post2.id)
        db.session.add(u1p2comment1)
        db.session.add(u1p2comment2)
        db.session.add(u1p2like1)
        db.session.add(u1p2like2)
        db.session.commit()

        u2p1comment1 = Comments(user4.id, u2post1.id, "I usually get the bus to workkk")
        u2p1comment2 = Comments(user3.id, u2post1.id, "Trains ftwwwwww")
        u2p1like1 = Likes(user1.id, u2post1.id)
        u2p1like2 = Likes(user2.id, u2post1.id)
        u2p1like3 = Likes(user4.id, u2post1.id)
        db.session.add(u2p1like1)
        db.session.add(u2p1like2)
        db.session.add(u2p1like3)
        db.session.add(u2p1comment1)
        db.session.add(u2p1comment2)
        db.session.commit()

        u3p1comment1 = Comments(user2.id, u3post1.id, "heard you took a veggie cooking class there, why vegetarian? thats not natural, eat some meat!")
        u3p1comment2 = Comments(user3.id, u3post1.id, "Its so much better for the environment though!!!!!")
        u3p1comment3 = Comments(user1.id, u3post1.id, "HEY! my partners veggie cooking is lovely.")
        u3p1like1 = Likes(user3.id, u3post1.id)
        u3p1like2 = Likes(user1.id, u3post1.id)
        db.session.add(u3p1comment1)
        db.session.add(u3p1comment2)
        db.session.add(u3p1comment3)
        db.session.add(u3p1like1)
        db.session.add(u3p1like2)
        db.session.commit()

        u3p2comment1 = Comments(user4.id, u3post2.id, "YOU'RE THE PERSON WHO HAS BEEN BUYING ALL OF THE CORN ON THE COB FROM THE SHOPS")
        u3p2like1 = Likes(user1.id, u3post2.id)
        u3p2like2 = Likes(user2.id, u3post2.id)
        u3p2like3 = Likes(user3.id, u3post2.id)
        u3p2like4 = Likes(user4.id, u3post2.id)
        db.session.add(u3p2comment1)
        db.session.add(u3p2like1)
        db.session.add(u3p2like2)
        db.session.add(u3p2like3)
        db.session.add(u3p2like4)
        db.session.commit()

        u4p1comment1 = Comments(user3.id, u4post1.id, "hmmm, i dont know.....")
        u4p1comment2 = Comments(user1.id, u4post1.id, "ITS ALICE SHE EATS SO MUCH CORN")
        u4p1comment3 = Comments(user2.id, u4post1.id, "whta is corn even made of??? you chew it and swallow it but then it comes out in corn shaped peices?!? WHAT IS THE SECRET! WHAT IS IT!?!??")
        u4p1like1 = Likes(user1.id, u4post1.id)
        u4p1like2 = Likes(user2.id, u4post1.id)
        u4p1like3 = Likes(user3.id, u4post1.id)
        db.session.add(u4p1comment1)
        db.session.add(u4p1comment2)
        db.session.add(u4p1comment3)
        db.session.add(u4p1like1)
        db.session.add(u4p1like2)
        db.session.add(u4p1like3) 
        db.session.commit()
