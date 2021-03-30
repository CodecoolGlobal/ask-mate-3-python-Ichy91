import os

from psycopg2.extras import RealDictCursor

import database_common


@database_common.connection_handler
def get_all_user_story(cursor: RealDictCursor) -> list:
    query = """
    SELECT * FROM question
    ORDER BY submission_time DESC
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
def update_user_data(cursor: RealDictCursor, title, message, image, question_id):
    query = """
    UPDATE question 
    SET title = %s, message = %s, image = %s 
    WHERE id = %s
            """
    cursor.execute(query, [title, message, image, question_id])


@database_common.connection_handler
def get_all_user_answer(cursor: RealDictCursor) -> list:
    query = """
    SELECT * 
    FROM answer
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def add_new_answer(cursor: RealDictCursor, date: str, question_id, message: str, image: str) -> list:
    query = """
    INSERT INTO answer(submission_time, vote_number, question_id, message, image)
    VALUES (%s, 0, %s, %s, %s)
    """
    cursor.execute(query, [date, question_id, message, image])


@database_common.connection_handler
def update_user_answer(cursor: RealDictCursor, update_answer:str) -> list:
    query = """
    UPDATE answer
    SET message = %s
    """
    cursor.execute(query, [update_answer])


@database_common.connection_handler
def get_next_question_id(cursor: RealDictCursor) -> list:
    query = """
    SELECT MAX(id)
    FROM question
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def question_vote(cursor: RealDictCursor, vote_number, question_id) -> list:
    query = """
    UPDATE question
    SET vote_number = %s
    WHERE id = %s
    """
    cursor.execute(query, [vote_number, question_id])


@database_common.connection_handler
def answer_vote(cursor: RealDictCursor, vote_number, question_id) -> list:
    query = """
    UPDATE answer
    SET vote_number = %s
    WHERE id = %s
    """
    cursor.execute(query, [vote_number, question_id])


@database_common.connection_handler
def delete_question(cursor: RealDictCursor, question_id) -> list:
    query = """
    DELETE FROM question
    WHERE id = %s
    
    """
    cursor.execute(query, [question_id])


@database_common.connection_handler
def delete_answers_by_question(cursor: RealDictCursor, question_id) -> list:
    query = """
    DELETE FROM answer
    WHERE question_id = %s

    """
    cursor.execute(query, [question_id])


@database_common.connection_handler
def delete_answer(cursor: RealDictCursor, answer_id) -> list:
    query = """
    DELETE FROM answer
    WHERE id = %s
    """
    cursor.execute(query, [answer_id])


@database_common.connection_handler
def view_counter(cursor: RealDictCursor, view_number, question_id) -> list:
    query = """
    UPDATE question 
    SET view_number = %s
    WHERE id = %s
    """
    cursor.execute(query, [view_number, question_id])


@database_common.connection_handler
def get_search_result_questions_id(cursor: RealDictCursor, phrase: str) -> list:
    query = """
    SELECT id
    FROM question
    WHERE LOWER(title) LIKE %s OR LOWER(message) like %s
    """
    cursor.execute(query, ['%'+phrase+'%', '%'+phrase+'%'])
    return cursor.fetchall()


@database_common.connection_handler
def get_search_result_questions_id_of_answers(cursor: RealDictCursor, phrase: str) -> list:
    query = """
    SELECT question_id as id
    FROM answer
    WHERE LOWER(message) like %s
    """
    cursor.execute(query, ['%'+phrase+'%'])
    return cursor.fetchall()
