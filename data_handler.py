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



@database_common.connection_handler
def get_all_user_answer(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM answer
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def add_new_answer(cursor: RealDictCursor, date: str, vote_number: str, question_id, message: str,
                   image: str) -> list:
    query = """
        INSERT INTO answer(submission_time,vote_number,question_id,message,image)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, [date, vote_number, question_id, message,
                   image])
    return cursor.fetchall()


@database_common.connection_handler
def update_user_answer(cursor: RealDictCursor, update_answer:str) -> list:
    query = """
    UPDATE answer
    SET message = %s
    """
    cursor.execute(query, [update_answer])
    return cursor.fetchall()

