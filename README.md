COLLEGE ENQUIRY CHATBOT
INSTRUCTION MANUAL
   ----------

     step-1

PRE-REQUISITES
Install the following libraries:  pip install Flask
 pip install chatterbot
 pip install chatterbot-corpus 
 pip install -U pip setuptools wheel
 pip install -U spacy
 python -m spacy download en_core_web_sm
 pip install Flask-reCaptcha
 pip install mysql-connector-python
 pip install mysql-connector-python-rf


      step-2

DATABASE STRUCTURE
1. Create Database
Query - create database register;
2. Create Table Users
Query - create table users(name varchar(30), email varchar(30), password 
varchar(15));
3. Create Table suggestion
Query - create table suggestion(email varchar(30), message varchar(255));


       step-3

Step by Step Instruction to follow to run the project

1. Load the project folder in an editor(VSC)
2. Install all the required libraries mentioned above and create the database 
structure in any database of your choice. (Change the connection statements 
according to the database you are using).
3. On the terminal locate your project directory.
4. In order to run the project, give the command
python app.py runserver
5. Paste the link in the browser of your choice.
6. Create an account through register page and login to the system.
7. Ask your question!
8. Logout of the system once done.
