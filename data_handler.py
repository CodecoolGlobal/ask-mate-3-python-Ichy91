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
    ORDER BY submission_time DESC
    LIMIT 5
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def add_new_question(cursor: RealDictCursor, time, title, message, image, user_id) -> list:
    query = """
    INSERT INTO question (submission_time, view_number, vote_number, title, message, image, user_id)
    VALUES(%s, 0, 0, %s, %s, %s, %s)
        """
    cursor.execute(query, [time, title, message, image, user_id])


@database_common.connection_handler
def add_new_answer(cursor: RealDictCursor, time, question_id, message, image, user_id) -> list:
    query = """
    INSERT INTO answer(submission_time, vote_number, question_id, message, image, user_id)
    VALUES (%s, 0, %s, %s, %s, %s)
    """
    cursor.execute(query, [time, question_id, message, image, user_id])


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
def add_comment_to_answer(cursor: RealDictCursor, answer_id, message, date, user_id) -> list:
    query = """
    INSERT INTO comment (answer_id, message, submission_time, edited_count, user_id)
    VALUES (%s, %s, %s, 0, %s)
    """
    cursor.execute(query, [answer_id, message, date, user_id])


@database_common.connection_handler
def add_new_comment_to_question(cursor: RealDictCursor, question_id,  message, submission_time, user_id) -> list:
    query = """
    INSERT INTO comment(question_id, message, submission_time, edited_count, user_id)
    VALUES (%s, %s, %s, 0, %s)
    """
    cursor.execute(query, [question_id, message, submission_time, user_id])


@database_common.connection_handler
def list_all_comments(cursor: RealDictCursor) -> list:
    query = """
    SELECT *
    FROM comment
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def update_comment(cursor: RealDictCursor, update_comment, updated_date, edited_count,  comment_id) -> list:
    query = """
    UPDATE comment
    SET message = %s, submission_time = %s, edited_count = %s
    WHERE id = %s
    """
    cursor.execute(query, [update_comment, updated_date, edited_count, comment_id])


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
        SELECT name, COUNT(name) AS occurence
        FROM tag
        GROUP BY name
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def add_new_user(cursor: RealDictCursor, username, hashed_password, date) -> list:
    query = """
    INSERT INTO users(name, password, created_date)
    VALUES (%s, %s, %s)
    """
    cursor.execute(query, [username, hashed_password, date])


@database_common.connection_handler
def count_user_activity(cursor: RealDictCursor) -> list:
    query = """
    SELECT users.id, COUNT(question.user_id) AS asked_question, 
    COUNT(answer.user_id) AS answered, COUNT(comment.user_id) as commented
    FROM users
    LEFT JOIN question ON question.user_id = users.id
    LEFT JOIN answer ON answer.user_id = users.id
    LEFT JOIN comment ON comment.user_id = users.id
    WHERE users.id = question.user_id OR users.id = answer.user_id OR users.id = comment.user_id
    GROUP BY users.id
    """
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