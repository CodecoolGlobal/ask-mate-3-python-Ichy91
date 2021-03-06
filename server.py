from flask import Flask, render_template, redirect, request, url_for, session
import data_handler, util, os
#from werkzeug.utils import secure_filename

app = Flask(__name__)
logged_in = False
app.secret_key = os.urandom(16)


@app.route("/")
def main_page():
    global logged_in
    questions = data_handler.get_five_latest_user_stories()
    users = data_handler.get_datas('users')

    if 'username' in session:
        return render_template("home.html", questions=questions, title="Home Page", login=logged_in, users=users)
    else:
        return render_template("home.html", questions=questions, title="Home Page", login=logged_in, users=users)


@app.route("/list")
def list_all_questions():
    global logged_in

    column_name = request.args.get('column-name')
    order_direction = request.args.get('order_direction')
    users = data_handler.get_datas('users')

    questions = util.get_questions_in_right_order(column_name, order_direction)

    return render_template("list.html", questions=questions, title="All questions", login=logged_in, users=users)


@app.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        datas_of_user = data_handler.get_datas_where('users', 'name', session['username'])

        if datas_of_user:
            user_password = util.get_right_data(datas_of_user, 'password')

            if util.verify_password(session['password'], user_password):
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
    questions = data_handler.get_datas_order_by_ASC('question', 'submission_time')
    answers = data_handler.get_datas_order_by_ASC('answer', 'submission_time')
    question_comment = data_handler.get_datas_where( 'comment', 'question_id', question_id)
    comments = data_handler.get_datas('comment')
    questions_tags = data_handler.get_datas('question_tag')
    tags = data_handler.get_datas('tag')
    users = data_handler.get_datas('users')

    data_handler.update_where('question', 'view_number', util.increase_view_number(questions, question_id), 'id', question_id)

    if logged_in:
        user_id = next(user['id'] for user in data_handler.get_datas('users') if session['username'] == user['name'])
        question_user_id = next(user['user_id'] for user in data_handler.get_datas_where('question', 'id', int(question_id)))

        if user_id == question_user_id:
            return render_template("display_question_by_owner.html", questions=questions, answers=answers,
                                   question_id=question_id, title="Post",
                                   question_comment=question_comment, comments=comments,
                                   questions_tags=questions_tags, tags=tags, users=users)

    return render_template("display_question.html", questions=questions, answers=answers,
                           question_id=question_id, title="Post",
                           question_comment=question_comment,comments=comments,
                           questions_tags=questions_tags, tags=tags, users=users)


@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    global logged_in

    if logged_in:
        if request.method == "POST":
            title = request.form["title"]
            message = request.form["message"]

            user_data = data_handler.get_datas_where('users', 'name', session['username'])
            user_id = util.get_right_data(user_data, 'id')

            if request.form["image"] == "":
                image = ""
            else:
                image = "images/" + request.form["image"]

            data_handler.add_new_question(title, message, image, user_id)

            return redirect(url_for("main_page"))

        else:
            return render_template("add_question.html", title="Add question")
    else:
        return redirect(url_for('main_page'))


@app.route("/question/<int:question_id>/new-answer", methods=["GET", "POST"])
def post_answer(question_id):
    global logged_in

    if logged_in:
        if request.method == "POST":
            answer = request.form["answer"]

            user_data = data_handler.get_datas_where('users', 'name', session['username'])
            user_id = util.get_right_data(user_data, 'id')

            if request.form["image"] == "":
                image = ""
            else:
                image = "images/" + request.form["image"]

            data_handler.add_new_answer(question_id, answer, image, user_id)

            return redirect(url_for("display_post", question_id=question_id))

        else:
            questions = data_handler.get_datas_order_by_ASC('question', 'submission_time')

            return render_template("post_answer.html", title="Post answer", questions=questions, question_id=question_id)
    else:
        return redirect(url_for('main_page'))


@app.route("/question/<int:question_id>/new-comment", methods=["GET","POST"])
def add_new_comment_to_question(question_id):
    questions = data_handler.get_datas_order_by_ASC('question', 'submission_time')
    global logged_in

    if logged_in:
        if request.method == 'POST':
            message = request.form['new-comment']

            user_data = data_handler.get_datas_where('users', 'name', session['username'])
            user_id = util.get_right_data(user_data, 'id')

            data_handler.add_new_comment_to_question(question_id, message, user_id)

            return redirect(url_for('display_post', question_id=question_id))

        return render_template('add_comment_question.html', questions=questions, question_id=question_id, title="Add comment")

    else:
        return redirect(url_for('main_page'))


@app.route("/answer/<int:answer_id>/new-comment", methods=["GET","POST"])
def add_answer_comment(answer_id):
    global logged_in

    if logged_in:
        answers = data_handler.get_datas_order_by_ASC('answer', 'submission_time')
        questions = data_handler.get_datas_order_by_ASC('answer', 'submission_time')

        question_id = next(answer['question_id'] for answer in answers if answer['id'] == answer_id)

        if request.method == "POST":
            message = request.form["new-comment"]

            user_data = data_handler.get_datas_where('users', 'name', session['username'])
            user_id = util.get_right_data(user_data, 'id')

            data_handler.add_comment_to_answer(answer_id, message, user_id)

            return redirect(url_for("display_post", question_id=question_id))

        return render_template("add_comment_answer.html", answers=answers, questions=questions, answer_id=answer_id, title="Add comment")

    else:
        return redirect(url_for('main_page'))


@app.route("/question/<int:question_id>/delete")
def delete_question(question_id):
    answers = data_handler.get_datas_order_by_ASC('answer', 'submission_time')
    correct_answer_ids = []
    global logged_in

    if logged_in:

        [correct_answer_ids.append(answer["id"]) for answer in answers if answer['question_id'] == question_id]
        [data_handler.delete('comment', 'answer_id', answer_id) for answer_id in correct_answer_ids]

        data_handler.delete('answer', 'question_id',question_id)
        data_handler.delete('comment', 'question_id', question_id)
        data_handler.delete('question_tag', 'question_id', question_id)

        data_handler.delete('question', 'id', question_id)

        return redirect(url_for("main_page"))
    else:
        return redirect(url_for("main_page"))


@app.route("/answer/<int:answer_id>/delete")
def delete_answer(answer_id):
    global logged_in

    if logged_in:
        answers = data_handler.get_datas_order_by_ASC('answer', 'submission_time')

        question_id = next(answer['question_id'] for answer in answers if answer['id'] == answer_id)

        data_handler.delete('comment', 'answer_id', answer_id)
        data_handler.delete('answer', 'id', answer_id)

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
            data_handler.update_user_data(updated_title, updated_message, image, question_id)

            return redirect(url_for("display_post", question_id=question_id))

        else:
            questions = data_handler.get_datas_order_by_ASC('question', 'submission_time')

            return render_template("edit_question.html", title="Edit question", questions=questions, question_id=question_id)
    else:
        return redirect(url_for('main_page'))


# Vote section
@app.route("/question/<int:question_id>/vote_up")
def question_vote_up(question_id):
    global logged_in

    if logged_in:

        questions = data_handler.get_datas_order_by_ASC('question', 'submission_time')
        user_id = util.get_right_data(data_handler.get_datas_where('question', 'id', int(question_id)), 'user_id')

        if user_id:
            user_details = data_handler.get_datas_where('users', 'id', int(user_id))
            reputation_number = next(user_detail['reputation'] for user_detail in user_details)
            data_handler.update_where('users', 'reputation', int(reputation_number) + 5, 'id', int(user_id))

        data_handler.update_where('question', 'vote_number', util.increase_vote_number(questions, question_id), 'id', question_id)

        return redirect(url_for("main_page"))

    else:
        return redirect(url_for("main_page"))


@app.route("/question/<int:question_id>/vote_down")
def question_vote_down(question_id):
    global logged_in

    if logged_in:
        questions = data_handler.get_datas_order_by_ASC('question', 'submission_time')
        user_id = next(user_id['user_id'] for user_id in data_handler.get_datas_where('question', 'id', int(question_id)))

        if user_id:
            user_details = data_handler.get_datas_where('users', 'id', int(user_id))
            reputation_number = next(user_detail['reputation'] for user_detail in user_details)
            data_handler.update_where('users', 'reputation', int(reputation_number) - 2, 'id', int(user_id))

        data_handler.update_where('question', 'vote_number', util.decrease_vote_number(questions, question_id), 'id', question_id)

        return redirect(url_for("main_page"))

    else:
        return redirect(url_for("main_page"))


@app.route("/answer/<int:answer_id>/vote_up")
def answer_vote_up(answer_id):
    global logged_in

    if logged_in:
        answers = data_handler.get_datas_order_by_ASC('answer', 'submission_time')

        user_id_dict = data_handler.get_datas_where('answer', 'id', int(answer_id))
        user_id = next(user_id['user_id'] for user_id in user_id_dict)

        if user_id:
            user_details = data_handler.get_datas_where('users', 'id', int(user_id))
            reputation_number = next(user_detail['reputation'] for user_detail in user_details)
            data_handler.update_where('users', 'reputation', int(reputation_number) + 10, 'id', int(user_id))

        data_handler.update_where('answer', 'vote_number', util.increase_vote_number(answers, answer_id), 'id', answer_id)
        question_id = util.get_question_id_by_answers(answers, answer_id)

        return redirect(url_for("display_post", question_id=question_id))
    else:
        return redirect(url_for('main_page'))


@app.route("/answer/<int:answer_id>/vote_down")
def answer_vote_down(answer_id):
    global logged_in

    if logged_in:
        answers = data_handler.get_datas_order_by_ASC('answer', 'submission_time')

        user_id_dict = data_handler.get_datas_where('answer', 'id', int(answer_id))
        user_id = next(user_id['user_id'] for user_id in user_id_dict)

        if user_id:
            user_details = data_handler.get_datas_where('users', 'id', int(user_id))
            reputation_number = next(user_detail['reputation'] for user_detail in user_details)
            data_handler.update_where('users', 'reputation', int(reputation_number) - 2, 'id', int(user_id))

        question_id = util.get_question_id_by_answers(answers, answer_id)
        data_handler.update_where('answer', 'vote_number', util.decrease_vote_number(answers, answer_id), 'id', answer_id)

        return redirect(url_for("display_post", question_id=question_id))
    else:
        return redirect(url_for('main_page'))


@app.route('/search')
def search_phrase():
    phrase = str(request.args.get('phrase')).lower()

    questions = data_handler.get_datas_order_by_ASC('question', 'submission_time')
    answers = data_handler.get_datas_order_by_ASC('answer', 'submission_time')

    extended_id_list = (data_handler.get_search_result_questions_id(phrase)+
                        data_handler.get_search_result_questions_id_of_answers(phrase))

    right_ids = {element['id'] for element in extended_id_list}

    return render_template('searched_questions.html', phrase=phrase, questions=questions, ids=right_ids, answers=answers, title="Search")


@app.route("/answer/<int:answer_id>/edit", methods=["GET","POST"])
def edit_answer(answer_id):
    global logged_in

    if logged_in:
        answers = data_handler.get_datas_order_by_ASC('answer', 'submission_time')
        questions = data_handler.get_datas_order_by_ASC('answer', 'submission_time')
        question_id = util.get_question_id_by_answers(answers, answer_id)

        if request.method == "POST":
            message = request.form["updated-answer"]

            if request.form["image"] == "":
                image = ""
            else:
                image = "images/"+request.form["image"]

            data_handler.update_user_answer(message, image, answer_id)

            return redirect(url_for("display_post", question_id=question_id))

        return render_template("edit_answer.html", answers=answers, questions=questions, answer_id=answer_id, question_id=question_id, title="Edit answer")
    else:
        return redirect(url_for('main_page'))


@app.route("/comment/<int:comment_id>/edit", methods=["GET","POST"])
def edit_comment(comment_id):
    global logged_in

    if logged_in:
        comments = data_handler.get_datas('comment')
        questions = data_handler.get_datas_order_by_ASC('question', 'submission_time')
        answers = data_handler.get_datas_order_by_ASC('answer', 'submission_time')

        if request.method == "POST":
            message = request.form["updated-comment"]

            data_handler.update_comment(message, util.give_edit_counter_right_value(comments, comment_id), comment_id)
            question_id = util.get_question_id_by_comments(comments, comment_id)
            return redirect(url_for("display_post", question_id=question_id))

        return render_template("edit_comment.html", comment_id=comment_id, comments=comments,
                               questions=questions, answers=answers, title="Edit comment")
    else:
        return redirect(url_for('main_page'))


@app.route("/comments/<int:comment_id>/delete")
def delete_comment(comment_id):
    global logged_in

    if logged_in:
        questions = data_handler.get_datas_order_by_ASC('question', 'submission_time')
        answers = data_handler.get_datas_order_by_ASC('answer', 'submission_time')
        comments = data_handler.get_datas('comment')

        for comment in comments:

            for question in questions:
                if question["id"] == comment["question_id"]:
                    question_id = question["id"]

            for answer in answers:
                if answer["id"] == comment["answer_id"]:
                    question_id = answer["question_id"]

        data_handler.delete('comment', 'id', comment_id)

        return redirect(url_for("display_post", question_id=question_id))
    else:
        return redirect(url_for('main_page'))


@app.route("/tags")
def list_tags():
    tags_and_occurence = data_handler.tags_and_occurence()

    return render_template('display_tags.html', tags=tags_and_occurence, title="Tags")


@app.route("/question/<int:question_id>/new-tag", methods=["GET", "POST"])
def add_question_tag(question_id):
    global logged_in

    if logged_in:
        try:
            tags = data_handler.get_datas('tag')
            if request.method == 'POST':
                if 'new-tag' in request.form:
                    for tag in tags:
                        if tag['name'] == request.form['new-tag']:
                            return render_template('adding_tag.html', tags=tags,  question_id=question_id)

                    data_handler.add_new_tag(request.form['new-tag'])
                    new_tag_id = data_handler.get_max_datas('id', 'tag')
                    data_handler.insert_new_ids(question_id, new_tag_id[0]['max'])

                elif 'existing-tags' in request.form:
                    existing_tag = request.form['existing-tags']
                    existing_tag_id = data_handler.get_datas_where_select('id', 'tag', 'name', existing_tag)
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
            unique = next(False if user['name'] == username else True for user in data_handler.get_datas('users'))

            if unique:
                data_handler.add_new_user(username, util.hash_password(request.form['password1']))
                return redirect(url_for('main_page'))

            return render_template('register_page.html', error_message = "ERROR: Username already in use!", title="Register")

        return render_template('register_page.html', error_message = "ERROR: Passwords do not match!", title="Register")

    return render_template('register_page.html', error_message = "", title="Register")


@app.route("/users")
def list_users():
    if session:
        count_activity = data_handler.count_user_activity()
        return render_template('list_users.html', count_activity=count_activity, title="Users")

    return redirect(url_for('main_page'))


@app.route("/user/<int:user_id>")
def get_user_data_by_id(user_id):
    comments = data_handler.get_datas('comment')
    questions = data_handler.get_datas_order_by_ASC('question', 'submission_time')
    answers = data_handler.get_datas_order_by_ASC('answer', 'submission_time')
    count_activity = data_handler.count_user_activity()

    return render_template('list_user_by_id.html', count_activity=count_activity,
                           questions=questions, comments=comments, answers=answers, user_id=user_id,
                           title="User panel")


@app.route("/answer/<int:question_id>/accept_answer", methods = ["POST"])
def accept_answer(question_id):
    global logged_in

    if logged_in:
        accepted_answer_ids = request.form.getlist('accepted')

        answer_ids_dict = data_handler.get_datas_where_select('id', 'answer', 'question_id', int(question_id))
        answer_ids = [id['id'] for id in answer_ids_dict]
        unaccepted_answer_ids = [id for id in answer_ids if str(id) not in accepted_answer_ids]

        for answer_id in accepted_answer_ids:

            data_handler.update_where('answer', 'accepted', True, 'id', answer_id)

            user_id = next(user_id['user_id'] for user_id in data_handler.get_datas_where_select('user_id', 'answer', 'id', int(answer_id)))
            user_details = data_handler.get_datas_where('users', 'id', int(user_id))
            reputation_number = next(user_detail['reputation'] for user_detail in user_details)

            data_handler.update_where('users', 'reputation', int(reputation_number) + 15, 'id', answer_id)

        for answer_id in unaccepted_answer_ids:
            data_handler.update_where('answer', 'accepted', False, 'id', answer_id)

    return redirect(url_for('display_post', question_id=question_id))


if __name__ == '__main__':
    app.run(
    debug=True,
    )