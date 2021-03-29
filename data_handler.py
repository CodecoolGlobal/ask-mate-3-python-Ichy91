import os

from psycopg2.extras import RealDictCursor

import database_common

QUESTION = "sample_data/question.csv"
QUESTION_HEADER = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER = "sample_data/answer.csv"
ANSWER_HEADER = ["id", "submission_time", "vote_number", "question_id", "message", "image"]


@database_common.connection_handler
def get_all_user_story(cursor: RealDictCursor) -> list:
    query = """
            SELECT * FROM question
    """
    cursor.execute(query)
    return cursor.fetchall()


def get_user_data(data):
    with open(QUESTION, "a") as add_obj:
        dict_writer = DictWriter(add_obj, fieldnames=QUESTION_HEADER)
        dict_writer.writerow(data) #if writerows it won't work


def update_user_data(data):
    with open(QUESTION, "w") as update_obj:
        dict_writer = csv.DictWriter(update_obj, fieldnames=QUESTION_HEADER)
        dict_writer.writeheader()
        dict_writer.writerows(data)


def get_all_user_answer():
    with open(ANSWER, "r") as read_obj:
        dict_reader = DictReader(read_obj)
        list_of_data = list(dict_reader)

    return list_of_data


def get_user_answer(data):
    with open(ANSWER, "a") as add_obj:
        dict_writer = DictWriter(add_obj, fieldnames=ANSWER_HEADER)
        dict_writer.writerow(data) #if writerows it won't work


def update_user_answer(data):
    with open(ANSWER, "w") as update_obj:
        dict_writer = csv.DictWriter(update_obj, fieldnames=ANSWER_HEADER)
        dict_writer.writeheader()
        dict_writer.writerows(data)

