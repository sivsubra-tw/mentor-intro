from flask import Flask, render_template, request, session
from flask_session import Session

import random

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

## Initial setup ##

engine = create_engine("postgres://wdaxldtkybvwcx:9ff8c1a17a091e693fec57232719724089da53603f754a26c05ddb316695e32d@ec2-176-34-183-20.eu-west-1.compute.amazonaws.com:5432/d77jf4piv3tg8t") #For DB connection
db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


## Fetch all questions of each category from the DB ##

all_questions = []

for i in range(3):
	questions_in_category = []
	rows = db.execute("SELECT question FROM questions WHERE category = (:category)",{"category":i}).fetchall()
	for each_row in rows:
		questions_in_category.append(each_row.question)
	print(questions_in_category)
	all_questions.append(questions_in_category)


## Utility functions ##

def reset():
	session.clear()
	session["questions_so_far"] =[] #Maintains a pair list of category, question
	session["questions_id"] = [random.randint(0,4),random.randint(0,4),random.randint(0,4)] #Maintains starting index of each category
	session["categories_so_far"] = [0,0,0] #Maintains a questions counter for each category



## Flask routes ##

@app.route("/")
def index():
	if session.get("questions_so_far") is None:
		reset()
	return render_template("index.html", questions_so_far = session["questions_so_far"], categories_so_far = session["categories_so_far"], start_timer = False)


@app.route("/", methods=["POST"])
def question():
	category = int(request.form.get("category"))

	if category == 3 or session.get("questions_id") is None:
		session.clear()
		reset()
		return render_template("index.html", questions_so_far = session["questions_so_far"], categories_so_far = session["categories_so_far"])

	else :
		session["questions_id"][category] += 1
		session["questions_id"][category] %= 5
		session["categories_so_far"][category] += 1

		curr_question_id = session["questions_id"][category]
		curr_question = all_questions[category][curr_question_id]
		session["questions_so_far"].append((category,curr_question))

		return render_template("index.html", curr_question = curr_question, category = category, questions_so_far = session["questions_so_far"], 
				categories_so_far = session["categories_so_far"], start_timer = True)

@app.route("/summary")
def logout():
	if session.get("questions_so_far") is not None:
		questions_so_far = session["questions_so_far"]
		session.clear()
		first = []
		second = []
		third = []
		for category, question in questions_so_far:
			if category == 0:
				first.append(question)
			elif category == 1:
				second.append(question)
			else:
				third.append(question)
		return render_template("summary.html", first = first, second = second, third = third, start_timer = False)
	else:
		return render_template("expired.html")
	