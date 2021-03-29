import os

from psycopg2.extras import RealDictCursor

import database_common


@database_common.connection_handler
def get_all_user_story(cursor: RealDictCursor) -> list:
    query = """
            SELECT * FROM question
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def add_new_question(cursor: RealDictCursor, time, title, message, image) -> list:

    query = """
                INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                VALUES(%s, 0, 0, %s, %s, %s)
        """
    cursor.execute(query, [time, title, message, image])


@database_common.connection_handler
def update_user_data(cursor: RealDictCursor, title, message, image):
    query = """
                    UPDATE question 
                    SET title = %s , message = %s, image = %s 
            """
    cursor.execute(query, [title, message, image])


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

