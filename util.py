import bcrypt
import data_handler


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


def get_questions_in_right_order(column_name, order_direction):
    return (data_handler.order_list_descending(column_name) if column_name and order_direction == 'DESC'
            else data_handler.order_list_ascending(column_name) if column_name and order_direction == 'ASC'
            else data_handler.get_all_user_story())


def get_right_data(datas, data_type):
    return next(data[data_type] for data in datas)


def get_question_id_by_answers(answers, answer_id):
    return next(answer['question_id'] for answer in answers if answer['id'] == answer_id)


def increase_view_number(questions, question_id):
    return next(question['view_number'] + 1 for question in questions if question['id'] == question_id)


def increase_vote_number(datas, id):
    return next(int(data["vote_number"]) + 1 for data in datas if data['id'] == id)


def decrease_vote_number(datas, id):
    return next(int(data["vote_number"]) - 1 for data in datas if data['id'] == id)


def give_edit_counter_right_value(comments, comment_id):
    return next(int(comment["edited_count"]) + 1 for comment in comments if comment['id'] == comment_id)
