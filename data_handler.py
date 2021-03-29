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


@database_common.connection_handler
def update_user_answer(cursor: RealDictCursor, update_answer:str) -> list:
    query = """
    UPDATE answer
    SET message = %s
    """
    cursor.execute(query, [update_answer])

