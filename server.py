from flask import Flask, render_template, redirect, request, url_for, session
import data_handler, util, os, datetime
#from werkzeug.utils import secure_filename

now_time = datetime.datetime.now()
app = Flask(__name__)
logged_in = False
app.secret_key = os.urandom(16)


@app.route("/")
def main_page():
    global logged_in
    questions = data_handler.get_five_latest_user_stories()
    users = data_handler.list_users()

    if 'username' in session:
        return render_template("home.html", questions=questions, title="Home Page", login=logged_in, users=users)
    else:
        return render_template("home.html", questions=questions, title="Home Page", login=logged_in, users=users)


@app.route("/list")
def list_all_questions():
    global logged_in

    column_name = request.args.get('column-name')
    order_direction = request.args.get('order_direction')
    users = data_handler.list_users()

    if column_name and order_direction == 'DESC':
        questions = data_handler.order_list_descending(column_name)
    elif column_name and order_direction == 'ASC':
        questions = data_handler.order_list_ascending(column_name)
    else:
        questions = data_handler.get_all_user_story()

    return render_template("list.html", questions=questions, title="All questions", login=logged_in, users=users)


@app.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        datas_of_user = data_handler.get_data_by_username(session['username'])

        if datas_of_user:
            for data_of_user in datas_of_user:
                users_password = data_of_user['password']

            if util.verify_password(session['password'], users_password):
                global logged_in
                logged_in = True

                return redirect(url_for('main_page'))

        return render_template('login.html', title="Login", error='ERROR: Invalid login attempt!')

    return render_template('login.html', title="Login")


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    global logged_in
    logged_in = False
    return redirect(url_for('main_page'))


@app.route("/question/<int:question_id>")
def display_post(question_id):
    global logged_in
    questions = data_handler.get_all_user_story()
    answers = data_handler.get_all_user_answer()
    question_comment = data_handler.list_question_comment(question_id)
    comments = data_handler.list_all_comments()
    questions_tags = data_handler.question_tags()
    tags = data_handler.get_tags()
    users = data_handler.list_users()

    for question in questions:
        if question['id'] == question_id:
            view_number = question['view_number'] + 1
        # view_number
    data_handler.view_counter(view_number, question_id)

    if logged_in:
        user_id = next(user['id'] for user in data_handler.list_users() if session['username'] == user['name'])
        question_user_id = next(user['user_id'] for user in data_handler.get_data_by_question_id(question_id))

        if user_id == question_user_id:
            return render_template("display_question_by_owner.html", questions=questions, answers=answers,
                                   question_id=question_id, title="Post",
                                   question_comment=question_comment, comments=comments,
                                   questions_tags=questions_tags, tags=tags, users=users)

    return render_template("display_question.html", questions=questions, answers=answers,
                           question_id=question_id, title="Post",
                           question_comment=question_comment,comments=comments,
                           questions_tags=questions_tags, tags=tags, users=users)


@app.route("/add-question", methods=["GET","POST"])
def add_question():
    global logged_in

    if logged_in:
        if request.method == "POST":
            title = request.form["title"]
            message = request.form["message"]
            time = now_time.strftime("%Y/%m/%d %H:%M:%S")
            user = data_handler.get_data_by_username(session['username'])

            for data in user:
                user_id = data['id']

            if request.form["image"] == "":
                image = ""
            else:
                image = "images/" + request.form["image"]

            data_handler.add_new_question(time, title, message, image, user_id)

            return redirect(url_for("main_page"))

        else:
            return render_template("add_question.html", title="Add question")
    else:
        return redirect(url_for('main_page'))


@app.route("/question/<int:question_id>/new-answer", methods=["GET","POST"])
def post_answer(question_id):
    global logged_in

    if logged_in:
        if request.method == "POST":
            answer = request.form["answer"]
            time = now_time.strftime("%Y/%m/%d %H:%M:%S")

            user = data_handler.get_data_by_username(session['username'])

            for data in user:
                user_id = data['id']

            if request.form["image"] == "":
                image = ""
            else:
                image = "images/" + request.form["image"]

            data_handler.add_new_answer(time, question_id, answer, image, user_id)

            return redirect(url_for("display_post", question_id=question_id))

        else:
            questions = data_handler.get_all_user_story()

            return render_template("post_answer.html", title="Post answer", questions=questions, question_id=question_id)
    else:
        return redirect(url_for('main_page'))


@app.route("/question/<int:question_id>/new-comment", methods=["GET","POST"])
def add_new_comment_to_question(question_id):
    questions = data_handler.get_all_user_story()
    global logged_in

    if logged_in:
        if request.method == 'POST':
            time = now_time.strftime("%Y/%m/%d %H:%M:%S")
            message = request.form['new-comment']
            user = data_handler.get_data_by_username(session['username'])

            for data in user:
                user_id = data['id']

            data_handler.add_new_comment_to_question(question_id, message, time, user_id)

            return redirect(url_for('display_post', question_id=question_id))

        return render_template('add_comment_question.html', questions=questions, question_id=question_id, title="Add comment")

    else:
        return redirect(url_for('main_page'))


@app.route("/answer/<int:answer_id>/new-comment", methods=["GET","POST"])
def add_answer_comment(answer_id):
    global logged_in

    if logged_in:
        answers = data_handler.get_all_user_answer()
        questions = data_handler.get_all_user_answer()

        for index in range(len(answers)):
            question_id = answers[index]["question_id"]

        if request.method == "POST":
            time = now_time.strftime("%Y/%m/%d %H:%M:%S")
            message = request.form["new-comment"]
            user = data_handler.get_data_by_username(session['username'])

            for data in user:
                user_id = data['id']

            data_handler.add_comment_to_answer(answer_id, message, time, user_id)

            return redirect(url_for("display_post", question_id=question_id))

        return render_template("add_comment_answer.html", answers=answers, questions=questions, answer_id=answer_id, title="Add comment")

    else:
        return redirect(url_for('main_page'))


@app.route("/question/<int:question_id>/delete")
def delete_question(question_id):
    answers = data_handler.get_all_user_answer()
    correct_answer_ids = []
    global logged_in

    if logged_in:
        for answer in answers:
            if answer["question_id"] == question_id:
                correct_answer_ids.append(answer["id"])

        for answer_id in correct_answer_ids:
            data_handler.delete_comment(answer_id)

        data_handler.delete_answers_by_question(question_id)
        data_handler.delete_comment_question(question_id)
        data_handler.delete_tag_before_delete_question(question_id)

        data_handler.delete_question(question_id)

        return redirect(url_for("main_page"))
    else:
        return redirect(url_for("main_page"))


@app.route("/answer/<int:answer_id>/delete")
def delete_answer(answer_id):
    global logged_in

    if logged_in:
        answers = data_handler.get_all_user_answer()

        for answer in answers:
            if answer["id"] == answer_id:
                question_id = answer["question_id"]

        data_handler.delete_comment(answer_id)
        data_handler.delete_answer(answer_id)

        return redirect(url_for("display_post", question_id=question_id))
    else:
        return redirect(url_for('main_page'))


@app.route("/question/<int:question_id>/edit", methods=["GET","POST"])
def edit_question(question_id):
    global logged_in

    if logged_in:
        if request.method == "POST":
            updated_title = request.form["title"]
            updated_message = request.form["message"]

            if request.form["image"] == "":
                image = ""
            else:
                image = "images/"+request.form["image"]
            #updating
            data_handler.update_user_data(updated_title,updated_message,image, question_id)

            return redirect(url_for("display_post", question_id=question_id))

        else:
            questions = data_handler.get_all_user_story()

            return render_template("edit_question.html", title="Edit question", questions=questions, question_id=question_id,)
    else:
        return redirect(url_for('main_page'))


# Vote section
@app.route("/question/<int:question_id>/vote_up")
def question_vote_up(question_id):
    global logged_in

    if logged_in:

        questions = data_handler.get_all_user_story()
        user_id_dict = data_handler.get_data_by_question_id(question_id)
        user_id = next(user_id['user_id'] for user_id in user_id_dict)

        if user_id:
            user_details = data_handler.get_data_by_user_id(user_id)
            reputation_number = next(user_detail['reputation'] for user_detail in user_details)
            data_handler.change_user_reputation(user_id, reputation_number + 5)

        for question in questions:
            if question["id"] == question_id:
                vote_number = int(question["vote_number"]) + 1

        data_handler.question_vote(vote_number, question_id)

        return redirect(url_for("main_page"))

    else:
        return redirect(url_for("main_page"))


@app.route("/question/<int:question_id>/vote_down")
def question_vote_down(question_id):
    global logged_in

    if logged_in:
        questions = data_handler.get_all_user_story()
        user_id_dict = data_handler.get_data_by_question_id(question_id)
        user_id = next(user_id['user_id'] for user_id in user_id_dict)

        if user_id:
            user_details = data_handler.get_data_by_user_id(user_id)
            reputation_number = next(user_detail['reputation'] for user_detail in user_details)
            data_handler.change_user_reputation(user_id, reputation_number - 2)

        for question in questions:
            if question["id"] == question_id:
                vote_number = int(question["vote_number"]) - 1

        data_handler.question_vote(vote_number, question_id)

        return redirect(url_for("main_page"))

    else:
        return redirect(url_for("main_page"))


@app.route("/answer/<int:answer_id>/vote_up")
def answer_vote_up(answer_id):
    global logged_in

    if logged_in:
        answers = data_handler.get_all_user_answer()

        user_id_dict = data_handler.get_data_by_answer_id(answer_id)
        user_id = next(user_id['user_id'] for user_id in user_id_dict)

        if user_id:
            user_details = data_handler.get_data_by_user_id(user_id)
            reputation_number = next(user_detail['reputation'] for user_detail in user_details)
            data_handler.change_user_reputation(user_id, reputation_number + 10)

        for answer in answers:
            if answer['id'] == answer_id:
                question_id = answer["question_id"]

        for answer in answers:
            if answer["id"] == answer_id:
                vote_number = int(answer["vote_number"]) + 1

        data_handler.answer_vote(vote_number, answer_id)

        return redirect(url_for("display_post", question_id=question_id))
    else:
        return redirect(url_for('main_page'))


@app.route("/answer/<int:answer_id>/vote_down")
def answer_vote_down(answer_id):
    global logged_in

    if logged_in:
        answers = data_handler.get_all_user_answer()

        user_id_dict = data_handler.get_data_by_answer_id(answer_id)
        user_id = next(user_id['user_id'] for user_id in user_id_dict)

        if user_id:
            user_details = data_handler.get_data_by_user_id(user_id)
            reputation_number = next(user_detail['reputation'] for user_detail in user_details)
            data_handler.change_user_reputation(user_id, reputation_number - 2)

        for answer in answers:
            if answer['id'] == answer_id:
                question_id = answer["question_id"]

        for answer in answers:
            if answer["id"] == answer_id:
                vote_number = int(answer["vote_number"]) - 1

        data_handler.answer_vote(vote_number, answer_id)

        return redirect(url_for("display_post", question_id=question_id))
    else:
        return redirect(url_for('main_page'))


@app.route('/search')
def search_phrase():
    phrase = str(request.args.get('phrase')).lower()

    questions = data_handler.get_all_user_story()
    answers = data_handler.get_all_user_answer()

    extended_id_list = (data_handler.get_search_result_questions_id(phrase)+
                        data_handler.get_search_result_questions_id_of_answers(phrase))

    right_ids = []
    for element in extended_id_list:
        if element['id'] not in right_ids:
            right_ids.append(element['id'])

    return render_template('searched_questions.html', phrase=phrase, questions=questions, ids=right_ids, answers=answers, title="Search")


@app.route("/answer/<int:answer_id>/edit", methods=["GET","POST"])
def edit_answer(answer_id):
    global logged_in

    if logged_in:
        answers = data_handler.get_all_user_answer()
        questions = data_handler.get_all_user_answer()

        for answer in answers:
            if answer["id"] == answer_id:
                question_id = answer["question_id"]

        if request.method == "POST":
            message = request.form["updated-answer"]

            if request.form["image"] == "":
                image = ""
            else:
                image = "images/"+request.form["image"]

            data_handler.update_user_answer(message,image,answer_id)

            return redirect(url_for("display_post", question_id=question_id))

        return render_template("edit_answer.html", answers=answers, questions=questions, answer_id=answer_id, question_id=question_id, title="Edit answer")
    else:
        return redirect(url_for('main_page'))


@app.route("/comment/<int:comment_id>/edit", methods=["GET","POST"])
def edit_comment(comment_id):
    global logged_in

    if logged_in:
        comments = data_handler.list_all_comments()
        questions = data_handler.get_all_user_story()
        answers = data_handler.get_all_user_answer()

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

            # return redirect(url_for("display_post", question_id=question_id))
            return redirect(url_for("main_page"))

        return render_template("edit_comment.html", comment_id=comment_id, comments=comments,
                               questions=questions, answers=answers, title="Edit comment")
    else:
        return redirect(url_for('main_page'))


@app.route("/comments/<int:comment_id>/delete")
def delete_comment(comment_id):
    global logged_in

    if logged_in:
        questions = data_handler.get_all_user_story()
        answers = data_handler.get_all_user_answer()
        comments = data_handler.list_all_comments()

        for comment in comments:
            for question in questions:
                if question["id"] == comment["question_id"]:
                    question_id = question["id"]

            for answer in answers:
                if answer["id"] == comment["answer_id"]:
                    question_id = answer["question_id"]

        data_handler.delete_comment_id(comment_id)

        return redirect(url_for("display_post", question_id=question_id))
    else:
        return redirect(url_for('main_page'))


@app.route("/tags")
def list_tags():
    tags_and_occurence = data_handler.tags_and_occurence()

    return render_template('display_tags.html', tags=tags_and_occurence, title="Tags")


@app.route("/question/<int:question_id>/new-tag", methods=["GET","POST"])
def add_question_tag(question_id):
    global logged_in

    if logged_in:
        try:
            tags = data_handler.get_tags()
            if request.method == 'POST':
                if 'new-tag' in request.form:
                    for tag in tags:
                        if tag['name'] == request.form['new-tag']:
                            return render_template('adding_tag.html', tags=tags,  question_id=question_id)

                    data_handler.add_new_tag(request.form['new-tag'])
                    new_tag_id = data_handler.max_tag_id()
                    data_handler.insert_new_ids(question_id, new_tag_id[0]['max'])

                elif 'existing-tags' in request.form:
                    existing_tag = request.form['existing-tags']
                    existing_tag_id = data_handler.get_id_to_tag(existing_tag)
                    data_handler.insert_new_ids(question_id, existing_tag_id[0]['id'])

                return redirect(url_for('display_post', question_id=question_id))

            return render_template('adding_tag.html', tags=tags,  question_id=question_id)

        except:
            return redirect(url_for('display_post', question_id=question_id))

    else:
        return redirect(url_for('main_page'))


@app.route("/question/<int:question_id>/tag/<int:tag_id>/delete")
def delete_tag(question_id,tag_id):
    global logged_in

    if logged_in:
        data_handler.delete_tags(question_id, tag_id)

        return redirect(url_for("display_post", question_id=question_id))
    else:
        return redirect(url_for('main_page'))


@app.route("/registration", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.form['password1'] == request.form['password2']:
            username = request.form['username']
            password = util.hash_password(request.form['password1'])
            users = data_handler.list_users()
            date = now_time.strftime("%Y/%m/%d %H:%M:%S")
            unique = True

            for user in users:
                if user['name'] == username:
                    unique = False

            if unique:
                data_handler.add_new_user(username, password, date)
                return redirect(url_for('main_page'))

            return render_template('register_page.html', error_message = "ERROR: Username already in use!", title="Register")

        return render_template('register_page.html', error_message = "ERROR: Passwords do not match!", title="Register")

    return render_template('register_page.html', error_message = "", title="Register")


@app.route("/users")
def list_users():
    #if session:
    count_activity = data_handler.count_user_activity()

    return render_template('list_users.html', count_activity=count_activity, title="Users")
    #return redirect(url_for('main_page'))


@app.route("/user/<int:user_id>")
def get_user_data_by_id(user_id):
    comments = data_handler.list_all_comments()
    questions = data_handler.get_all_user_story()
    answers = data_handler.get_all_user_answer()
    count_activity = data_handler.count_user_activity()

    question_id = 0

    # for comment in comments:
    #     if user_id == comment['user_id']:
    #         question_id = comment['question_id']
    #         print(question_id)
    #
    # for answer in answers:
    #     if user_id == answer['user_id']:
    #         question_id = answer['question_id']
    #         print(question_id)
    #
    # for question in questions:
    #     if user_id == question['user_id']:
    #         question_id = question['id']
    #         print(question_id)

    return render_template('list_user_by_id.html', count_activity=count_activity,
                           questions=questions, comments=comments, answers=answers, user_id=user_id,
                           question_id=question_id, title="User panel")


@app.route("/answer/<int:question_id>/accept_answer", methods = ["POST"])
def accept_answer(question_id):
    global logged_in

    if logged_in:
        accepted_answer_ids = request.form.getlist('accepted')

        answer_ids_dict = data_handler.get_all_answers_of_a_question(question_id)
        answer_ids = [id['id'] for id in answer_ids_dict]
        unaccepted_answer_ids = [id for id in answer_ids if str(id) not in accepted_answer_ids]

        for answer_id in accepted_answer_ids:

            data_handler.update_answered_status(answer_id, True)

            user_id = next(user_id['user_id'] for user_id in data_handler.get_user_id_by_answer_id(answer_id))
            user_details = data_handler.get_data_by_user_id(user_id)
            reputation_number = next(user_detail['reputation'] for user_detail in user_details)

            data_handler.change_user_reputation(user_id, reputation_number + 15)

        for answer_id in unaccepted_answer_ids:
            data_handler.update_answered_status(answer_id, False)

    return redirect(url_for('display_post', question_id=question_id))


if __name__ == '__main__':
    app.run(
    debug=True,
    )