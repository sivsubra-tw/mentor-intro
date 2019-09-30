from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route("/")
def index():
	questions_so_far = []
	return render_template("index.html")


questions = [
			 ['Tell me about a time when everything went wrong. How did you deal with it?', 
			  'Describe a moment when you felt like you truly achieved something',
			  'What is your favourite childhood memory?'],
			 ['Are there times when you feel like you do not like your job? If yes, what do you do then?', 
			  'What is something you wish you knew before you started your career?', 
			  'Have you ever had conflict with a colleague? How did you deal with it?'],
			 ['What is your favourite hobby?', 
			  'Do you have a role model? If yes, who is it? If no, why not?', 
			  'Is there a book or movie that you think changed you as a person?']
			]

questions_id = [random.randint(0,2),random.randint(0,2),random.randint(0,2)]
questions_so_far = []
categories_so_far = [0,0,0]

@app.route("/", methods=["POST"])
def question():
	category = int(request.form.get("category"))

	questions_id[category] += 1
	questions_id[category] %= 3
	categories_so_far[category] += 1

	if categories_so_far[category] <= 3:
		questions_so_far.append(category)

	return render_template("index.html", question = questions[category][questions_id[category]], questions_so_far = questions_so_far)