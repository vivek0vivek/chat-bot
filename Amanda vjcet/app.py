from flask import Flask, render_template, request, session, redirect, flash
from flask_recaptcha import ReCaptcha
import mysql.connector
import os
from chatterbot import ChatBot
from jinja2 import Markup
from chatterbot.trainers import ListTrainer
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# nltk.download('stopwords')

bot = ChatBot('<b>Amanda Bot</b>')
bot = ChatBot(
    'ChatBot for College Enquiry',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': "Hi there, Welcome to VJCET Chat Bot 👋 If you need any assistance, I'm always here.Go ahead and write the number of any query. 😃✨<b><br><br>  Which of the following user groups do you belong to? <br><br>1.&emsp;Student's Section Enquiry.</br>2.&emsp;Faculty Section Enquiry. </br>3.&emsp;Parent's Section Enquiry.</br>4.&emsp;Visitor's Section Enquiry.</br><br>",
            'maximum_similarity_threshold': 0.90
        }
    ],
    database_uri='sqlite:///database.sqlite3'
)

trainer = ListTrainer(bot)

conversation = [
"Hi",
"Helloo!",

"hey",
"im here.",

"what courses are available",
"computer engineering, electronics and computer science, Mechanical Engineering, Science and Humanities, AI & Data Science",


"how are you?",
"I'm good.</br> <br>Go ahead and write the number of any query. 😃✨ <br> 1.&emsp;Student's Section Enquiry.</br>2.&emsp;Faculty Section Enquiry. </br>3.&emsp;Parent's Section Enquiry.</br>4.&emsp;Visitor's Section Enquiry.</br>",

"great",
"Go ahead and write the number of any query. 😃✨ <br> 1.&emsp;Student's Section Enquiry.</br>2.&emsp;Faculty Section Enquiry. </br>3.&emsp;Parent's Section Enquiry.</br>4.&emsp;Visitor's Section Enquiry.</br>",

"good",
"Go ahead and write the number of any query. 😃✨ <br> 2.&emsp;Faculty Section Enquiry. </br>3.&emsp;Parent's Section Enquiry.</br>4.&emsp;Visitor's Section Enquiry.</br>",

"fine",
"Go ahead and write the number of any query. 😃✨ <br> 2.&emsp;Faculty Section Enquiry. </br>3.&emsp;Parent's Section Enquiry.</br>4.&emsp;Visitor's Section Enquiry.</br>",

"thank You",
"Your Welcome 😄",

"thanks",
"Your Welcome 😄",

"bye",
"Thank You for visiting!..",

"what do you do",
"I am made to give Information about Viswajothi College Of Engineering Vazhakulam.",

"what else can you do",
"I can help you know more about VJCET",

"how long will be B-tech course",
"Our college offers 4 year long B-tech course",

"location",
"vazhakulam,ernakulam,kerala,india",

"course duration",
"Our college offers 4 year long B-tech course",

"semesters",
"There are two semesters in a year.",

"sem duration",
"The single semester will be around 4 months",

"admission requirements",
"Candidates those who score an aggregate of at least 45% marks in Mathematics, Physics and Chemistry  in plus two examination are eligible",

"classes",
"There may be six classes per day. Each class will be of 55 minutes.",

"teaching style",
"Our college has different teaching patterns than other colleges of kerala. We following the LTW techniques which stands for Lecture, Tutorial and Workshop.\nYou can provide us with your contact details and our counselors shall reach out to you and provide you with further details.",

"exams",
"The model involves both internal assessment as well as written exam. The internal assignment will include projects, practical, assignments etc, Normally 30% is allocated to this section and the rest will be for the written exam.",

"hours",
"You can message us here at any hours. But our college premises will be open from 8:00 am to 5:00 pm only",

"fun activites",
"Yes, Of course. Our college not only provides excellent education but also encourage students to take part in different curriculum activities. The college conducts yearly programs like Sports meet, Carnival, Holi festival, and Christmas. \n Also our college has basketball court, badminton court, table tennis, chess, carrom board and many more refreshment zones.",

"facilities",
"With excellent education facilities, Our College provides various other facilities like 24 hours internet, library, canteen, parking space, and student service for any students queries.",

"fee",
"The fees for the college is INR 73500 in the first year of education. So, for 4 years of education, the amount in around INR 294000. The amount can be feasible for some but can also be expensive for other students.",

"",
"Sorry, can't understand you",

"invalid",
"Please give me more info",
    
    "1",
    "<b>STUDENT <br>The following are frequently searched terms related to student . Please select one from the options below : <br> <br> 1.1 Departments <br>1.2 Curriculars<br>1.3  Administrative<br>1.4 Extra-Curriculars</b>",
    
    "1.1",
    "<b>  DEPARTMENTS <br>  These are the top results: <br> <br> 1.1.1 ARTIFICIAL INTELLIGENCE AND DATA SCIENCE <br> 1.1.2 CIVIL ENGINEERING <br> 1.1.3 COMPUTER SCIENCE & DESIGN <br> 1.1.4 COMPUTER SCIENCE & ENGINEERING<br> 1.1.5 ELECTRONICS & COMMUNICATION ENGINEERING<br> 1.1.6 ELECTRICAL & ELECTRONICS ENGINEERING<br> 1.1.7 INFORMATION TECHNOLOGY<br> 1.1.8 MECHANICAL ENGINEERING<br> 1.1.9 HOTEL MANAGEMENT & CATERING TECHNOLOGY<br> 1.1.10 MANAGEMENT STUDIES<br> 1.1.11 SCIENCE & HUMANITIES</b>",
    "1.1.1",
    "<b> 1.1.1 ARTIFICIAL INTELLIGENCE AND DATA SCIENCE <br>The link 👉 <a href=" 'https://vjcet.org/departments/artificial-intelligence-and-data-science' ">Click Here</a> </b>",
    "1.1.2",
    "<b > 1.1.2 CIVIL ENGINEERING <br>The link 👉<a href=" 'https://vjcet.org/departments/civil-engineering' ">Click Here</a> </b>",
    "1.1.3",
    "<b> 1.1.3 COMPUTER SCIENCE & DESIGN <br>The link 👉 <a href=" 'https://vjcet.org/departments/computer-science-and-design' ">Click Here</a> </b>",
    "1.1.4",
    "<b> 1.1.4 COMPUTER SCIENCE & ENGINEERING <br>The link 👉 <a href=" 'https://vjcet.org/departments/computer-science-and-engineering' ">Click Here</a> </b>",
     "1.1.5",
    "<b> 1.1.5 ELECTRONICS & COMMUNICATION ENGINEERING <br>The link to 👉 <a href=" 'https://vjcet.org/departments/electronics-and-communication-engineering' ">Click Here</a> </b>",
     "1.1.6",
    "<b> 1.1.6 ELECTRICAL & ELECTRONICS ENGINEERING <br>The link 👉 <a href=" 'https://vjcet.org/departments/electrical-and-electronics-engineering' ">Click Here</a> </b>",
     "1.1.7",
    "<b> 1.1.7 INFORMATION TECHNOLOGY <br>The link 👉 <a href=" 'https://vjcet.org/departments/information-technology' ">Click Here</a> </b>",
     "1.1.8",
    "<b> 1.1.8 MECHANICAL ENGINEERING <br>The link 👉 <a href=" 'https://vjcet.org/departments/mechanical-engineering' ">Click Here</a> </b>",
     "1.1.9",
    "<b> 1.1.9 HOTEL MANAGEMENT & CATERING TECHNOLOGY <br>The link 👉 <a href=" 'https://vjcet.org/departments/hotel-management-and-catering-technology' ">Click Here</a> </b>",
     "1.1.10",
    "<b> 1.1.10 MANAGEMENT STUDIES <br>The link 👉 <a href=" 'https://vjcet.org/departments/Management%20Studies' ">Click Here</a> </b>",
     "1.1.11",
    "<b> 1.1.11 SCIENCE & HUMANITIES <br>The link 👉 <a href=" 'https://vjcet.org/departments/science-and-humanities' ">Click Here</a> </b>",

    "1.2",
    "<b>CURRICULARS<br>These are the top results: <br> <br> 1.2.1 ACADEMIC CALENDAR<br> 1.2.2 SYLLABUS AND CURRICULUM <br> 1.2.3 RULES & REGULATIONS <br> 1.2.4 ROLL OF HONOURS <br> 1.2.5 LIBRARY</b>",
    "1.2.1",
    "<b > 1.2.1 ACADEMIC CALENDAR<br>The link 👉 <a href=" 'https://vjcet.org/academic-calendar' ">Click Here</a></b>",
    "1.2.2",
    "<b > 1.2.2 SYLLABUS AND CURRICULUM<br>The link 👉<a href=" 'https://vjcet.org/syllabus-and-curriculum' ">Click Here</a> </b>",
    "1.2.3",
    "<b > 1.2.3 RULES & REGULATIONS<br>The link 👉 <a href=" 'https://vjcet.org/rules-and-regulations' ">Click Here</a> </b>",
    "1.2.4",
    "<b > 1.2.4 ROLL OF HONOURS<br>The link 👉 <a href=" 'https://vjcet.org/roll-of-honours' ">Click Here</a> </b>",
    "1.2.5",
    "<b > 1.2.5 LIBRARY<br>The link 👉 <a href=" 'https://vjcet.org/facilities/the-central-library' ">Click Here</a> </b>",

    "1.3",
    "<b>1.3 ADMINISTRATIVE<br>These are the top results: <br> <br> 1.3.1 STUDENTS PORTAL<br> 1.3.2 FEE PAYMENT<br> 1.3.3 AICTE Feedback </b>",
    "1.3.1",
    "<b> 1.3.1 STUDENTS PORTAL<br>The link 👉 <a href=" 'https://vjcet.etlab.in/user/login' ">Click Here</a> </b>",
    "1.3.2",
    "<b> 1.3.2 FEE PAYMENT<br>The link 👉 <a href=" 'https://vjcet.org/fee-payment' ">Click Here</a> </b>",
    "1.3.3",
    "<b> 1.3.3 AICTE Feedback FOR STUDENTS<br>The link 👉 <a href=" 'https://aicte-india.org/feedback/students.php' ">Click Here</a> </b>",

    "1.4",
    "<b > EXTRA-CURRICULARS <br>These are the top results:<br> 1.4.1 STUDENT COUNCIL<br> 1.4.2 DRISHYA <br> 1.4.3 DRONA<br> 1.4.4 BODHI<br> 1.4.5 PROFESSIONAL BODIES<br> 1.4.6 NATIONAL SERVICE SCHEME </b>",
    "1.4.1",
    "<b > 1.4.1 STUDENT COUNCIL<br>The link 👉 <a href=" 'https://vjcet.org/student-council' ">Click Here</a> </b>",
    "1.4.2",
    "<b > 1.4.2 DRISHYA<br>The link 👉<a href=" 'https://vjcet.org/drishya' ">Click Here</a> </b>",
    "1.4.3",
    "<b > 1.4.3 DRONA<br>The link 👉 <a href=" 'https://vjcet.org/drona' ">Click Here</a> </b>",
    "1.4.4",
    "<b > 1.4.4 BODHI<br>The link 👉 <a href=" 'https://vjcet.org/bodhi' ">Click Here</a> </b>",
    "1.4.5",
    "<b > 1.4.5 PROFESSIONAL BODIES<br>The link 👉 <a href=" 'https://vjcet.org/professional-bodies' ">Click Here</a> </b>",
    "1.4.6",
    "<b > 1.4.6 NATIONAL SERVICE SCHEME<br>The link 👉 <a href=" 'https://vjcet.org/national-service-scheme' ">Click Here</a> </b>",


    "2",
    "<b >FACULTY<br>The following are frequently searched terms related to faculty. Please select one from the options below :</br></br>2.1 VJCET FACULTY PORTAL<br>2.2 UNIVERSITY EXAMINATION SEAT ARRAGEMENT<br>2.3 LIBRARY<br>2.4 PTA </b>",
    
    "2.1",
    "<b> 2.1 VJCET FACULTY PORTAL<br>The link 👉<a href=" 'https://vjcet.etlab.in/user/login' ">Click Here</a> </b>",
    "2.2",
    "<b> 2.2 UNIVERSITY EXAMINATION SEAT ARRAGEMENT<br>The link 👉<a href=" 'http://117.239.154.84:8001/ktuexam/index.html' ">Click Here</a> </b>",
    "2.3",
    "<b> 2.3 LIBRARY<br>The link 👉<a href=" 'https://vjcet.org/facilities/the-central-library' ">Click Here</a> </b>",
    "2.4",
    "<b> 2.4 P.T.A<br>The link 👉<a href=" 'https://vjcet.org/parent-teacher-association-pta' ">Click Here</a> </b>",
  
    "3",
    "<b >PARENTS<br>The following are frequently searched terms related to parents. Please select one from the options below :</br></br>3.1 PTA<br>3.2 CAMPUS MAP<br>3.3 FACILITIES<br>3.4 ACADEMIC PERFORMANCE<br>3.5 FEE PAYMENT </b>",
    
    "3.1",
    "<b> 3.1 PTA<br>The link 👉<a href=" 'https://vjcet.org/parent-teacher-association-pta' ">Click Here</a> </b>",
    "3.2",
    "<b> 3.2 CAMPUS MAP<br>The link 👉<a href=" 'https://vjcet.org/campus-map' ">Click Here</a> </b>",
    "3.3",
    "<b> 3.3 FACILITIES<br>The link 👉<a href=" 'https://vjcet.org/facilities' ">Click Here</a> </b>",
    "3.4",
    "<b> 3.4 ACADEMIC PERFORMANCE<br>The link 👉<a href=" 'https://vjcet.org/academic-performance' ">Click Here</a> </b>",
    "3.5",
    "<b> 3.5 FEE PAYMENT<br>The link 👉<a href=" 'https://vjcet.org/fee-payment' ">Click Here</a> </b>",
    
    "4",
    "<b >VISITORS<br>The following are frequently searched terms related to visitors. Please select one from the options below :</br></br>4.1 ABOUT VISWAJYOTHI<br>4.2 FOUNDERS<br>4.3 AFFILIATIONS & ACCREDITATIONS<br>4.4 FACILITIES<br>4.5 CONTACT US<br>4.6 COURSES OFFERED<br>4.7 PLACEMENT AND TRAINING<br>4.8 RESEARCH & DEVELOPMENT </b>",
    
    "4.1",
    "<b> 4.1 ABOUT VISWAJYOTHI<br>The link 👉<a href=" 'https://vjcet.org/about' ">Click Here</a> </b>",
    "4.2",
    "<b> 4.2 FOUNDERS<br>The link 👉<a href=" 'https://vjcet.org/founders' ">Click Here</a> </b>",
    "4.3",
    "<b> 4.3 AFFILIATIONS & ACCREDITATIONS<br>The link 👉<a href=" 'https://vjcet.org/affiliations-and-accreditations' ">Click Here</a> </b>",
    "4.4",
    "<b> 4.4 FACILITIES<br>The link 👉<a href=" 'https://vjcet.org/facilities' ">Click Here</a> </b>",
    "4.5",
    "<b> 4.5 CONTACT US<br>The link 👉<a href=" 'https://vjcet.org/contact' ">Click Here</a> </b>",
    "4.6",
    "<b> 4.6 COURSES OFFERED<br>The link 👉<a href=" 'https://vjcet.org/courses-offered' ">Click Here</a> </b>",
    "4.7",
    "<b> 4.7 PLACEMENT AND TRAINING<br>The link 👉<a href=" 'https://vjcet.org/certification-and-placements' ">Click Here</a> </b>",
    "4.8",
    "<b> 4.8 RESEARCH & DEVELOPMENT<br>The link 👉<a href=" 'https://vjcet.org/research-and-development' ">Click Here</a> </b>",
    

]

trainer.train(conversation)

app = Flask(__name__)
recaptcha = ReCaptcha(app)
app.secret_key=os.urandom(24)
app.static_folder = 'static'

app.config.update(dict(
    RECAPTCHA_ENABLED = True,
    RECAPTCHA_SITE_KEY = "6LdbAx0aAAAAAANl04WHtDbraFMufACHccHbn09L",
    RECAPTCHA_SECRET_KEY = "6LdbAx0aAAAAAMmkgBKJ2Z9xsQjMD5YutoXC6Wee"
))

recaptcha=ReCaptcha()
recaptcha.init_app(app)

app.config['SECRET_KEY'] = 'cairocoders-ednalan'

conn=mysql.connector.connect(host='localhost',port='3306',user='root',password='root',database='register',auth_plugin='mysql_native_password')
cur=conn.cursor()

@app.route("/index")
def home():
    if 'id' in session:
        return render_template('index.html')
    else:
        return redirect('/')

@app.route('/')
def login():
    return render_template("login.html")

@app.route('/register')
def about():
    return render_template('register.html')

@app.route('/forgot')
def forgot():
    return render_template('forgot.html')

@app.route('/login_validation',methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')

    cur.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email,password))
    users = cur.fetchall()
    if len(users)>0:
        session['id']=users[0][0]
        flash('You were successfully logged in')
        return redirect('/index')
    else:
        flash('Invalid credentials !!!')
        return redirect('/')

@app.route('/add_user',methods=['POST'])
def add_user():
    name=request.form.get('name') 
    email=request.form.get('uemail')
    password=request.form.get('upassword')
    cur.execute("""INSERT INTO  users(name,email,password) VALUES('{}','{}','{}')""".format(name,email,password))
    conn.commit()
    cur.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
    myuser=cur.fetchall()
    flash('You have successfully registered!')
    session['id']=myuser[0][0]
    return redirect('/index')

@app.route('/suggestion',methods=['POST'])
def suggestion():
    email=request.form.get('uemail')
    suggesMess=request.form.get('message')
    cur.execute("""INSERT INTO  suggestion(email,message) VALUES('{}','{}')""".format(email,suggesMess))
    conn.commit()
    flash('You suggestion is succesfully sent!')
    return redirect('/index')

@app.route('/add_user',methods=['POST'])
def register():
    if recaptcha.verify():
        flash('New User Added Successfully')
        return redirect('/register')
    else:
        flash('Error Recaptcha') 
        return redirect('/register')

@app.route('/logout')
def logout():
    session.pop('id')
    return redirect('/')

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')  
    reply = bot.get_response(userText)
    print(reply)
    return str(reply)

if __name__ == "__main__":
    app.run() 