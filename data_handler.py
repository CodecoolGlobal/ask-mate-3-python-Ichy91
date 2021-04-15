import datetime
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs
from psycopg2.extras import RealDictCursor
import database_common


@database_common.connection_handler
def get_all_user_story(cursor: RealDictCursor) -> list:
    query = """
    SELECT * FROM question
    ORDER BY submission_time ASC
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_five_latest_user_stories(cursor: RealDictCursor) -> list:
    query = """
    SELECT * FROM question
    ORDER BY submission_time ASC
    LIMIT 5
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def add_new_question(cursor: RealDictCursor, title, message, image, user_id) -> list:
    query = """
    INSERT INTO question (submission_time, view_number, vote_number, title, message, image, user_id)
    VALUES(current_timestamp, 0, 0, %s, %s, %s, %s)
        """
    cursor.execute(query,[title, message, image, user_id])


@database_common.connection_handler
def add_new_answer(cursor: RealDictCursor, question_id, message, image, user_id) -> list:
    query = """
    INSERT INTO answer(submission_time, vote_number, question_id, message, image, user_id)
    VALUES (current_timestamp, 0, %s, %s, %s, %s)
    """
    cursor.execute(query, [question_id, message, image, user_id])


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
    ORDER BY submission_time
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def update_user_answer(cursor: RealDictCursor, message, image, answer_id) -> list:
    query = """
    UPDATE answer
    SET message = %s, image = %s
    WHERE id = %s
    """
    cursor.execute(query, [message, image, answer_id])


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
    WHERE title ilike %s OR message ilike %s
    """
    cursor.execute(query, ['%'+phrase+'%', '%'+phrase+'%'])
    return cursor.fetchall()


@database_common.connection_handler
def list_answer_comment(cursor: RealDictCursor, answer_id) -> list:
    query = """
    SELECT *
    FROM comment
    WHERE answer_id = %s
    """
    cursor.execute(query, [answer_id])
    return cursor.fetchall()


@database_common.connection_handler
def list_question_comment(cursor: RealDictCursor, question_id) -> list:
    query = """
    SELECT *
    FROM comment
    WHERE question_id = %s
    """
    cursor.execute(query, [question_id])
    return cursor.fetchall()


@database_common.connection_handler
def get_search_result_questions_id_of_answers(cursor: RealDictCursor, phrase: str) -> list:
    query = """
    SELECT question_id as id
    FROM answer
    WHERE message ilike %s 
    """
    cursor.execute(query, ['%'+phrase+'%'])
    return cursor.fetchall()


@database_common.connection_handler
def add_comment_to_answer(cursor: RealDictCursor, answer_id, message, user_id) -> list:
    query = """
    INSERT INTO comment (answer_id, message, submission_time, edited_count, user_id)
    VALUES (%s, %s, current_timestamp, 0, %s)
    """
    cursor.execute(query, [answer_id, message, user_id])


@database_common.connection_handler
def add_new_comment_to_question(cursor: RealDictCursor, question_id,  message, user_id) -> list:
    query = """
    INSERT INTO comment(question_id, message, submission_time, edited_count, user_id)
    VALUES (%s, %s, current_timestamp, 0, %s)
    """
    cursor.execute(query, [question_id, message, user_id])


@database_common.connection_handler
def list_all_comments(cursor: RealDictCursor) -> list:
    query = """
    SELECT *
    FROM comment
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def update_comment(cursor: RealDictCursor, update_comment, edited_count,  comment_id) -> list:
    query = """
    UPDATE comment
    SET message = %s, submission_time = current_timestamp, edited_count = %s
    WHERE id = %s
    """
    cursor.execute(query, [update_comment, edited_count, comment_id])


@database_common.connection_handler
def delete_comment(cursor: RealDictCursor, answer_id) -> list:
    query = """
    DELETE FROM comment
    WHERE answer_id = %s
    """
    cursor.execute(query, [answer_id])


@database_common.connection_handler
def delete_comment_id(cursor: RealDictCursor, comment_id) -> list:
    query = """
    DELETE FROM comment
    WHERE id = %s
    """
    cursor.execute(query, [comment_id])


@database_common.connection_handler
def delete_comment_question(cursor: RealDictCursor, question_id) -> list:
    query = """
    DELETE FROM comment
    WHERE question_id = %s
    """
    cursor.execute(query, [question_id])


@database_common.connection_handler
def question_tags(cursor: RealDictCursor) -> list:
    query = """
    SELECT *
    FROM question_tag
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_tags(cursor: RealDictCursor) -> list:
    query = """
    SELECT *
    FROM tag
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def delete_tags(cursor: RealDictCursor, question_id, tag_id) -> list:
    query = """
    DELETE FROM question_tag
    WHERE question_id = %s AND tag_id = %s
    """
    cursor.execute(query, [question_id, tag_id])


@database_common.connection_handler
def order_list_descending(cursor: RealDictCursor, column_name: str) -> list:
    query = sql.SQL(
        '''
        SELECT * 
        FROM question 
        ORDER BY {} DESC''').format(sql.Identifier(column_name))
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def order_list_ascending(cursor: RealDictCursor, column_name: str) -> list:
    query = sql.SQL(
        '''
        SELECT * 
        FROM question 
        ORDER BY {} ASC''').format(sql.Identifier(column_name))
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def add_new_tag(cursor: RealDictCursor, name: str) -> list:
    query = '''
        INSERT INTO tag(name) 
        VALUES (LOWER(%s))
        '''
    cursor.execute(query, [name])


@database_common.connection_handler
def insert_new_ids(cursor: RealDictCursor, question_id: int, tag_id: int) -> list:
    query = '''
        INSERT INTO question_tag(question_id, tag_id) 
        VALUES (%s, %s)
        '''
    cursor.execute(query, [question_id, tag_id])


@database_common.connection_handler
def max_tag_id(cursor: RealDictCursor) -> list:
    query = '''
        SELECT MAX(id) 
        FROM tag
        '''
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_id_to_tag(cursor: RealDictCursor, name: str) -> list:
    query = '''
        SELECT id
        FROM tag
        WHERE name = %s
        '''
    cursor.execute(query, [name])
    return cursor.fetchall()


@database_common.connection_handler
def delete_tag_before_delete_question(cursor: RealDictCursor, question_id) -> list:
    query = """
    DELETE FROM question_tag
    WHERE question_id = %s
    """
    cursor.execute(query, [question_id])


@database_common.connection_handler
def tags_and_occurence(cursor: RealDictCursor) -> list:
    query = """
        SELECT name, COUNT(question_tag.question_id) AS occurence
        FROM tag
        JOIN question_tag ON question_tag.tag_id = tag.id
        GROUP BY name
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def add_new_user(cursor: RealDictCursor, username, hashed_password) -> list:
    query = """
    INSERT INTO users(name, password, created_date, reputation)
    VALUES (%s, %s, current_timestamp, 0)
    """
    cursor.execute(query, [username, hashed_password])


@database_common.connection_handler
def count_user_activity(cursor: RealDictCursor) -> list:
    query = """
    SELECT id,name,created_date,
           CASE WHEN asked_question IS NULL THEN 0 ELSE asked_question END as asked_question,
           CASE WHEN answered IS NULL THEN 0 ELSE answered END as answered,
           CASE WHEN commented IS NULL THEN 0 ELSE commented END as commented,
           reputation
    FROM users

    LEFT JOIN(
        SELECT question.user_id,
               COUNT(question.user_id) AS asked_question
        FROM question
        GROUP BY user_id) question ON question.user_id = users.id

    LEFT JOIN(
        SELECT answer.user_id,
              COUNT(answer.user_id) AS answered
        FROM answer
        GROUP BY user_id) answer ON answer.user_id = users.id

    LEFT JOIN(
        SELECT comment.user_id,
               COUNT(comment.user_id) AS commented
        FROM comment
        GROUP BY user_id) comment ON comment.user_id = users.id

        ORDER BY id
    """
    """
    # SELECT id,name,created_date,
    #            CASE WHEN asked_question IS NULL THEN 0 ELSE asked_question END as asked_question,
    #            CASE WHEN answered IS NULL THEN 0 ELSE answered END as answered,
    #            CASE WHEN commented IS NULL THEN 0 ELSE commented END as commented,
    #            reputation
    #     FROM users
    # 
    #     LEFT JOIN(
    #         SELECT question.user_id,
    #                CASE WHEN question.user_id IS NULL THEN 0 ELSE COUNT(question.user_id) END AS asked_question
    #         FROM question
    #         GROUP BY user_id) question ON question.user_id = users.id
    # 
    #     LEFT JOIN(
    #         SELECT answer.user_id,
    #                CASE WHEN answer.user_id IS NULL THEN 0 ELSE COUNT(answer.user_id) END AS answered
    #         FROM answer
    #         GROUP BY user_id) answer ON answer.user_id = users.id
    # 
    #     LEFT JOIN(
    #         SELECT comment.user_id,
    #                CASE WHEN comment.user_id IS NULL THEN 0 ELSE COUNT(comment.user_id) END AS commented
    #         FROM comment
    #         GROUP BY user_id) comment ON comment.user_id = users.id
    #         
    #         ORDER BY id
    # """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def list_users(cursor: RealDictCursor) -> list:
    query = """
    SELECT *
    FROM users
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_data_by_username(cursor: RealDictCursor, username: str) -> list:
    query = """
        SELECT * FROM users
        WHERE name = %s
    """
    cursor.execute(query, [username])
    return cursor.fetchall()


@database_common.connection_handler
def get_data_by_user_id(cursor: RealDictCursor, user_id: int) -> list:
    query = """
        SELECT * FROM users
        WHERE id = %s
    """
    cursor.execute(query, [user_id, ])
    return cursor.fetchall()


@database_common.connection_handler
def get_data_by_answer_id(cursor: RealDictCursor, answer_id: int) -> list:
    query = """
        SELECT * FROM answer
        WHERE id = %s
    """
    cursor.execute(query, [answer_id, ])
    return cursor.fetchall()


@database_common.connection_handler
def get_data_by_question_id(cursor: RealDictCursor, question_id: int) -> list:
    query = """
        SELECT * FROM question
        WHERE id = %s
    """
    cursor.execute(query, [question_id])
    return cursor.fetchall()


@database_common.connection_handler
def change_user_reputation(cursor: RealDictCursor, user_id: int, reputation: int) -> list:
    query = """
            UPDATE users
            SET reputation = %s
            WHERE id = %s
        """
    cursor.execute(query, [reputation, user_id])


@database_common.connection_handler
def update_answered_status(cursor: RealDictCursor, answered_id: int, status: bool) -> list:
    query = """
               UPDATE answer
               SET accepted = %s
               WHERE id = %s
           """
    cursor.execute(query, [status, answered_id])


@database_common.connection_handler
def get_question_id_by_answer(cursor: RealDictCursor, answer_id: int) -> list:
    query = """
               SELECT question_id FROM answer
               WHERE id = %s
           """
    cursor.execute(query, [answer_id])
    return cursor.fetchall()


@database_common.connection_handler
def get_all_answers_of_a_question(cursor: RealDictCursor, question_id: int) -> list:
    query = """
               SELECT id FROM answer
               WHERE question_id = %s
           """
    cursor.execute(query, [question_id])
    return cursor.fetchall()


@database_common.connection_handler
def get_user_id_by_answer_id(cursor: RealDictCursor, answer_id: int) -> list:
    query = """
               SELECT user_id FROM answer
               WHERE id = %s
           """
    cursor.execute(query, [answer_id])
    return cursor.fetchall()