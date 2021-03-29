from flask import Flask, render_template, redirect, request, url_for
import data_handler, util
import datetime
import json
import os

app = Flask(__name__)
now_time = datetime.datetime.now()


@app.route("/")
def hello():
    return redirect(url_for("main_page"))

@app.route("/list")
def main_page():
    questions = data_handler.get_all_user_story()
    return render_template("list.html", questions=questions, title="Home Page")

@app.route("/list/<arg>/<check>")
def index_true(arg, check):
    questions = data_handler.get_all_user_story()
    if arg != []:
        util.sorting(questions,arg)
        if check != []:
            util.reverse(questions,check)

    return render_template("list.html", questions=questions, title="Home Page", arg=arg, check=check)

@app.route("/question/<question_id>")
#display the question and giving answer
def display_post(question_id):
    questions = data_handler.get_all_user_story()
    answers = data_handler.get_all_user_answer()
    #view_number
    questions[int(question_id)-1]["view_number"] = int(questions[int(question_id)-1]["view_number"]) + 1
    data_handler.update_user_data(questions)
    return render_template("display_question.html", questions=questions, answers=answers, question_id=question_id, title="{0}. Post".format(question_id))

@app.route("/add-question", methods=["GET","POST"])
def add_question():
    if request.method=="POST":
        questions = data_handler.get_all_user_story()


        title = request.form["title"]
        message = request.form["message"]
        time = now_time.strftime("%Y/%m/%d %H:%M:%S")

        if request.form["image"] == "":
            image = ""
        else:
            image = "/static/images/" + request.form["image"]

        data_handler.add_new_question(time, title, message, image)
        return redirect(url_for("main_page"))
    else:
        return render_template("add_question.html", title="Add question")

@app.route("/question/<question_id>/new-answer", methods=["GET","POST"])
def post_answer(question_id):
    if request.method == "POST":
        answers = data_handler.get_all_user_answer()
        answer_id = "0"
        for answer in answers:
            answer_id = answer["id"]
        answer = request.form["answer"] #id,submission_time,vote_number,question_id,message,image
        time = now_time.strftime("%Y/%m/%d %H:%M:%S")
        new_id = int(answer_id) + 1
        vote_number = 0
        if request.form["image"] == "":
            image = ""
        else:
            image = "/static/images/" + request.form["image"]
        new_answer = {"id":str(new_id),"submission_time":str(time),"vote_number":vote_number,"question_id":question_id,"message":answer,"image":image}
        data_handler.get_user_answer(new_answer)
        return redirect(url_for("display_post", question_id=question_id))
    else:
        questions = data_handler.get_all_user_story()
        return render_template("post_answer.html", title="Post comment", questions=questions, question_id=question_id)

@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    questions = data_handler.get_all_user_story()
    answers = data_handler.get_all_user_answer()
    delete_question = [question for question in questions if not (question['id'] == question_id)]
    delete_answer = [answer for answer in answers if not (answer['question_id'] == question_id)]

    for question_id, question in enumerate(delete_question, 1): #second element is the start value
        question["id"] = question_id
    for answer_id, answer in enumerate(delete_answer, 1):
        answer["id"] = answer_id

    data_handler.update_user_data(delete_question)
    data_handler.update_user_answer(delete_answer)
    return redirect(url_for("main_page"))

@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    answers = data_handler.get_all_user_answer()
    question_id = ""
    for index in range(len(answers)):
        question_id = answers[index]["question_id"]
        if answers[index]['id'] == answer_id:
            del answers[index]
            break

    for new_id, answer in enumerate(answers, 1):
        answer["id"] = new_id

    data_handler.update_user_answer(answers)
    return redirect(url_for("display_post", question_id=question_id))

@app.route("/question/<question_id>/edit", methods=["GET","POST"])
def edit_question(question_id):
    if request.method == "POST":
        questions = data_handler.get_all_user_story()
        questions[int(question_id)-1]["title"] = request.form["title"]
        questions[int(question_id)-1]["message"] = request.form["message"]
        if request.form["image"] == "":
            data_handler.update_user_data(questions)
        else:
            questions[int(question_id)-1]["image"] = "/static/images/"+request.form["image"]
            data_handler.update_user_data(questions)
        return redirect(url_for("display_post", question_id=question_id))
    else:
        questions = data_handler.get_all_user_story()
        return render_template("update.html", title="Update", questions=questions, question_id=question_id)

#Vote section
@app.route("/question/<question_id>/vote_up")
def question_vote_up(question_id):
    questions = data_handler.get_all_user_story()
    questions[int(question_id) - 1]["vote_number"] = int(questions[int(question_id) - 1]["vote_number"]) + 1
    data_handler.update_user_data(questions)
    return redirect(url_for("main_page"))

@app.route("/question/<question_id>/vote_down")
def question_vote_down(question_id):
    questions = data_handler.get_all_user_story()
    questions[int(question_id) - 1]["vote_number"] = int(questions[int(question_id) - 1]["vote_number"]) - 1
    data_handler.update_user_data(questions)
    return redirect(url_for("main_page"))

@app.route("/answer/<answer_id>/vote_up")
def answer_vote_up(answer_id):
    answers = data_handler.get_all_user_answer()
    question_id = ""
    for index in range(len(answers)):
        question_id = answers[index]["question_id"]
    answers[int(answer_id) -1]["vote_number"] = int(answers[int(answer_id) -1]["vote_number"]) + 1
    data_handler.update_user_answer(answers)
    return redirect(url_for("display_post", question_id=question_id))

@app.route("/answer/<answer_id>/vote_down")
def answer_vote_down(answer_id):
    answers = data_handler.get_all_user_answer()
    question_id = ""
    for index in range(len(answers)):
        question_id = answers[index]["question_id"]
    answers[int(answer_id) -1]["vote_number"] = int(answers[int(answer_id) -1]["vote_number"]) - 1
    data_handler.update_user_answer(answers)
    return redirect(url_for("display_post", question_id=question_id))


if __name__ == '__main__':
    app.run(
        debug=True,
    )