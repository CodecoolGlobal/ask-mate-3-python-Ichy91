from flask import Flask, render_template, redirect, request, url_for
import data_handler, util
import datetime
#from werkzeug.utils import secure_filename

now_time = datetime.datetime.now()
app = Flask(__name__)


@app.route("/")
@app.route("/list")
def main_page():

    questions = data_handler.get_all_user_story()
    return render_template("list.html", questions=questions, title="Home Page")

@app.route("/question/<int:question_id>")
def display_post(question_id):

    questions = data_handler.get_all_user_story()
    answers = data_handler.get_all_user_answer()
    #view_number
    return render_template("display_question.html", questions=questions, answers=answers, question_id=question_id, title="{0}. Post".format(question_id))

@app.route("/add-question", methods=["GET","POST"])
def add_question():

    if request.method=="POST":

        title = request.form["title"]
        message = request.form["message"]
        time = now_time.strftime("%Y/%m/%d %H:%M:%S")

        if request.form["image"] == "":
            image = ""
        else:
            image = "/static/images/" + request.form["image"]

        #image = my_request.form.files["image"]

        #upload_image = util.upload_file(image,next_id,"Q")

        data_handler.add_new_question(time, title, message, image)
        return redirect(url_for("main_page"))
    else:
        return render_template("add_question.html", title="Add question")

@app.route("/question/<int:question_id>/new-answer", methods=["GET","POST"])
def post_answer(question_id):

    if request.method == "POST":

        answer = request.form["answer"]
        time = now_time.strftime("%Y/%m/%d %H:%M:%S")

        if request.form["image"] == "":
            image = ""
        else:
            image = "/static/images/" + request.form["image"]

        data_handler.add_new_answer(time, question_id, answer, image)

        return redirect(url_for("display_post", question_id=question_id))
    else:
        questions = data_handler.get_all_user_story()
        return render_template("post_answer.html", title="Post comment", questions=questions, question_id=question_id)

#modify
@app.route("/question/<int:question_id>/delete")
def delete_question(question_id):

    questions = data_handler.get_all_user_story()
    answers = data_handler.get_all_user_answer()

    data_handler.update_user_data(delete_question)
    data_handler.update_user_answer(delete_answer)

    return redirect(url_for("main_page"))

#modify
@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):

    answers = data_handler.get_all_user_answer()
    question_id = ""

    data_handler.update_user_answer(answers)
    return redirect(url_for("display_post", question_id=question_id))

@app.route("/question/<int:question_id>/edit", methods=["GET","POST"])
def edit_question(question_id):

    if request.method == "POST":

        updated_title = request.form["title"]
        updated_message = request.form["message"]

        if request.form["image"] == "":
            image = ""
        else:
            image = "/static/images/"+request.form["image"]
        #updating
        data_handler.update_user_data(updated_title,updated_message,image, question_id)
        return redirect(url_for("display_post", question_id=question_id))
    else:
        questions = data_handler.get_all_user_story()
        return render_template("update.html", title="Update", questions=questions, question_id=question_id)

#Vote section
@app.route("/question/<int:question_id>/vote_up")
def question_vote_up(question_id):

    questions = data_handler.get_all_user_story()

    for question in questions:
        if question["id"] == question_id:
            vote_number = int(question["vote_number"]) + 1

    data_handler.question_vote(vote_number, question_id)

    return redirect(url_for("main_page"))

@app.route("/question/<int:question_id>/vote_down")
def question_vote_down(question_id):

    questions = data_handler.get_all_user_story()

    for question in questions:
        if question["id"] == question_id:
            vote_number = int(question["vote_number"]) -1

    data_handler.question_vote(vote_number,question_id)

    return redirect(url_for("main_page"))

@app.route("/answer/<int:answer_id>/vote_up")
def answer_vote_up(answer_id):

    answers = data_handler.get_all_user_answer()

    question_id = ""

    for index in range(len(answers)):
        question_id = answers[index]["question_id"]

    for answer in answers:
        if answer["id"] == answer_id:
            vote_number = int(answer["vote_number"]) + 1

    data_handler.answer_vote(vote_number,answer_id)

    return redirect(url_for("display_post", question_id=question_id))

@app.route("/answer/<int:answer_id>/vote_down")
def answer_vote_down(answer_id):

    answers = data_handler.get_all_user_answer()
    question_id = ""

    for index in range(len(answers)):
        question_id = answers[index]["question_id"]

    for answer in answers:
        if answer["id"] == answer_id:
            vote_number = int(answer["vote_number"]) - 1

    data_handler.answer_vote(vote_number, answer_id)

    return redirect(url_for("display_post", question_id=question_id))

if __name__ == '__main__':
    app.run(
        debug=True,
    )