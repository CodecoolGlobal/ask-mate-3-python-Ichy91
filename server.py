from flask import Flask, render_template, redirect, request, url_for
import data_handler, util
import datetime
#from werkzeug.utils import secure_filename

now_time = datetime.datetime.now()
app = Flask(__name__)


@app.route("/")
def main_page():
    questions = data_handler.get_five_latest_user_stories()

    return render_template("home.html", questions=questions, title="Home Page")


@app.route("/list")
def list_all_questions():
    questions = data_handler.get_all_user_story()

    return render_template("list.html", questions=questions, title="All questions")


@app.route("/question/<int:question_id>")
def display_post(question_id):
    questions = data_handler.get_all_user_story()
    answers = data_handler.get_all_user_answer()
    question_comment = data_handler.list_question_comment(question_id)
    comments = data_handler.list_all_comments()

    for question in questions:
        if question['id'] == question_id:
            view_number = question['view_number'] +1
    # view_number
    data_handler.view_counter(view_number, question_id)

    return render_template("display_question.html", questions=questions, answers=answers,
                           question_id=question_id, title="{0}. Post".format(question_id),
                           question_comment=question_comment,comments=comments)



@app.route("/add-question", methods=["GET","POST"])
def add_question():
    if request.method == "POST":
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


@app.route("/question/<int:question_id>/new-comment", methods=["GET","POST"])
def add_new_comment_to_question(question_id):
    questions = data_handler.get_all_user_story()

    if request.method == 'POST':
        time = now_time.strftime("%Y/%m/%d %H:%M:%S")
        message = request.form['new-comment']

        data_handler.add_new_comment_to_question(question_id, message, time)

        return redirect(url_for('display_post', question_id=question_id))

    return render_template('add_comment_question.html', questions=questions, question_id=question_id)


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


@app.route("/question/<int:question_id>/delete")
def delete_question(question_id):
    data_handler.delete_answers_by_question(question_id)
    data_handler.delete_question(question_id)

    return redirect(url_for("main_page"))


@app.route("/answer/<int:answer_id>/delete")
def delete_answer(answer_id):
    answers = data_handler.get_all_user_answer()

    for index in range(len(answers)):
        question_id = answers[index]["question_id"]

    data_handler.delete_answer(answer_id)

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

    for index in range(len(answers)):
        question_id = answers[index]["question_id"]

    for answer in answers:
        if answer["id"] == answer_id:
            vote_number = int(answer["vote_number"]) - 1

    data_handler.answer_vote(vote_number, answer_id)

    return redirect(url_for("display_post", question_id=question_id))


@app.route('/search')
def search_phrase():
    displayed_phrase = str(request.args.get('phrase'))
    phrase = displayed_phrase.lower()
    questions = data_handler.get_all_user_story()

    extended_id_list = (data_handler.get_search_result_questions_id(phrase)+
                        data_handler.get_search_result_questions_id_of_answers(phrase))

    right_ids = []
    for element in extended_id_list:
        if element['id'] not in right_ids:
            right_ids.append(element['id'])

    return render_template('searched_questions.html', phrase=displayed_phrase, questions=questions, ids=right_ids)


@app.route("/answer/<int:answer_id>/new-comment", methods=["GET","POST"])
def add_answer_comment(answer_id):

    answers = data_handler.get_all_user_answer()
    questions = data_handler.get_all_user_answer()

    for index in range(len(answers)):
        question_id = answers[index]["question_id"]

    if request.method == "POST":

        time = now_time.strftime("%Y/%m/%d %H:%M:%S")
        message = request.form["new-comment"]
        data_handler.add_comment_to_answer(answer_id,message,time)

        return redirect(url_for("display_post", question_id=question_id))

    return render_template("add_comment_answer.html", answers=answers, questions=questions, answer_id=answer_id)


@app.route("/answer/<int:answer_id>/edit", methods=["GET","POST"])
def edit_answer(answer_id):

    answers = data_handler.get_all_user_answer()
    questions = data_handler.get_all_user_answer()

    for index in range(len(answers)):
        question_id = answers[index]["question_id"]

    if request.method == "POST":

        message = request.form["updated-answer"]
        data_handler.update_answer(message,answer_id)

        return redirect(url_for("display_post", question_id=question_id))

    return render_template("edit_answer.html", answers=answers, questions=questions, answer_id=answer_id, question_id=question_id)


@app.route("/comment/<int:comment_id>/edit", methods=["GET","POST"])
def edit_comment(comment_id):

    comments = data_handler.list_all_comments()
    questions = data_handler.get_all_user_story()
    answers = data_handler.get_all_user_answer()

    for index in range(len(answers)):
        question_id = answers[index]["question_id"]

    if request.method == "POST":

        time = now_time.strftime("%Y/%m/%d %H:%M:%S")
        message = request.form["updated-comment"]


        for comment in comments:
            if comment["id"] == comment_id:
                if comment["edited_count"] == None:
                    edit_counter = 1
                else:
                    edit_counter = int(comment["edited_count"]) + 1


        data_handler.update_comment(message,time,edit_counter,comment_id)

        return redirect(url_for("display_post", question_id=question_id))

    return render_template("edit_comment.html", comment_id=comment_id, question_id=question_id, comments=comments,
                           questions=questions)


if __name__ == '__main__':
    app.run(
        debug=True,
    )