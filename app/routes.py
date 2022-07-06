import threading
from time import sleep
from app import app
from flask import render_template, request, redirect, url_for, session, g, flash
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm, QuestionForm
from app.models import User, Questions
from app import db
from flask import Flask, render_template, Response
import cv2
from faceapi import face_detect
import base64
import time

# app=Flask(__name__)
# camera = cv2.VideoCapture(1)
current_time=time.time()
previous_time=time.time()

@app.before_first_request
def before_first_request_func():

    global previous_time 
    previous_time=time.time()
    # print(previous_time)
    print("This function will run once")

@app.before_request
def before_request():
    g.user = None
    if "user_id" in session:
        user = User.query.filter_by(id=session["user_id"]).first()
        g.user = user
        if(request.path[1:9] == "question"):
            if(request.method == "GET"):
                print("Request path")
                print(request.path[10:11])
                global previous_time
                if(request.path[10:11]!="1"):
                    print()
                    print("HEYYYYYYYYYYYYYYYYYYYYYY")
                    print()
                    # print("Time taken to answer question : " + str(time.time()-g.rishit))
                    print("Time taken to answer question : " + str(time.time()-previous_time))
                    # g.risht=time.time()
                    previous_time=time.time()
                    # print(g.rishit)
                else:
                    print("First gstart!!!!")
                    previous_time=time.time()
                    g.rishit=time.time()

# @app.after_request
# def after_request(response):
#     print(request.path[1:9])
#     if(request.path[1:9] == "question"):
#         if(request.method == "POST"):
#             print("HEY")
#             print(type(g.start))
#             # print("start: ",g.start)
#             diff = time.time() - g.start
#             print("Time spent"  + str(diff))
#     if ((response.response) and
#         (200 <= response.status_code < 300) and
#         (response.content_type.startswith('text/html'))):
#         response.set_data(response.get_data().replace(
#             b'__EXECUTION_TIME__', bytes(str(0), 'utf-8')))
#     return response



@app.route("/")
def home():
    # db.session.query(Questions).delete()
    # db.session.commit()
    print(Questions.query.all())
    # question=Questions(q_id=6)
    question=Questions.query.get(5)
    print(question.scorea)
    question.ques="Why do you want to be IIITD Student Mentor?"
    question.a="I have maintained a good academic and extracurricular record so I think I’d have a lot to offer to the program."
    question.b="I am keen to pass on the college culture to the new students."
    question.c="I am inspired by my mentor who helped me adapt to the college and learn effectively."
    question.d="I’m looking for personal growth and development and to add some leadership experience to my resume."
    question.e="I have had a vast variety of experiences in college and I believe I can really help someone new adapt well and avoid the mistakes I made."
    question.f="I’m empathetic and easy to talk to so I’d help juniors assimilate with ease."
    question.scorea=2
    question.scoreb=5
    question.scorec=3
    question.scored=0
    question.scoree=5
    question.scoref=5
    # print(question.ques)
    # print(question.a)
    # db.session.add(question)
    # db.session.commit()
    return render_template("index.html", title="Home")




@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for("login"))
        session["user_id"] = user.id
        session["marks"] = 0
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("home")
        return redirect(next_page)
        return redirect(url_for("home"))
    if g.user:
        return redirect(url_for("home"))
    return render_template("login.html", form=form, title="Login")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.password.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.id
        session["marks"] = 0
        return redirect(url_for("home"))
    if g.user:
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)


def generate_frames():
    while True:
        camera = cv2.VideoCapture(1)
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode(".jpg", frame)
            img_bytes = base64.b64encode(buffer)
            frame = buffer.tobytes()
        print(face_detect(img_bytes, is_local=True))
        sleep(5)


threading_ = threading.Thread(target=generate_frames, daemon=True)
threading_.start()


@app.route("/video")
def video():
    return "VIDEO"


@app.route("/question/<int:id>", methods=["GET", "POST"])
def question(id):
    if(id==1):
        session["marks"]=0
    print(request.method, id)
    form = QuestionForm()
    q = Questions.query.filter_by(q_id=id).first()
    if not q:
        return redirect(url_for("score"))
    if not g.user:
        return redirect(url_for("login"))
    if request.method == "POST":
        option = request.form["options"]
        print("Option: ", option)
        if(option==q.a):
            session["marks"]+=q.scorea
        if(option==q.b):
            session["marks"]+=q.scoreb
        if(option==q.c):
            session["marks"]+=q.scorec
        if(option==q.d):
            session["marks"]+=q.scored
        if(option==q.e):
            session["marks"]+=q.scoree
        if(option==q.f):
            session["marks"]+=q.scoref
        # if option == q.ans:
        #     session["marks"] += 10
        return redirect(url_for("question", id=(id + 1)))
    form.options.choices = [(q.a, q.a), (q.b, q.b), (q.c, q.c), (q.d, q.d),(q.e, q.e),(q.f, q.f)]
    return render_template(
        "question.html", form=form, q=q, title="Question {}".format(id),number=id
    )


@app.route("/score")
def score():
    if not g.user:
        return redirect(url_for("login"))
    g.user.marks = session["marks"]
    # db.session.commit()
    return render_template("score.html", title="Final Score")


@app.route("/logout")
def logout():
    if not g.user:
        return redirect(url_for("login"))
    session.pop("user_id", None)
    session.pop("marks", None)
    return redirect(url_for("home"))
