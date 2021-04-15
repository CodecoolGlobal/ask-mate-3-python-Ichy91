from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import database_common


@database_common.connection_handler
def get_datas(cursor: RealDictCursor, table_name: str) -> list:
    query = sql.SQL(
        '''
        SELECT * 
        FROM {} ''').format(sql.Identifier(table_name))
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_datas_where(cursor: RealDictCursor, table_name: str, column_name: str, value) -> list:
    query = sql.SQL(
        '''
        SELECT * 
        FROM {table} 
        WHERE {column} = %s''').format(
        table = sql.Identifier(table_name),
        column = sql.Identifier(column_name))
    cursor.execute(query, [value])
    return cursor.fetchall()


@database_common.connection_handler
def get_datas_where_select(cursor: RealDictCursor, select: str,table_name: str, column_name: str, value) -> list:
    query = sql.SQL(
        '''
        SELECT {select} 
        FROM {table} 
        WHERE {column} = %s''').format(
        select = sql.Identifier(select),
        table = sql.Identifier(table_name),
        column = sql.Identifier(column_name))
    cursor.execute(query, [value])
    return cursor.fetchall()


@database_common.connection_handler
def get_datas_order_by_ASC(cursor: RealDictCursor, table_name: str, column_name: str) -> list:
    query = sql.SQL(
        '''
        SELECT * 
        FROM {table} 
        ORDER BY {column} ASC''').format(
        table = sql.Identifier(table_name),
        column = sql.Identifier(column_name))
    cursor.execute(query)
    return cursor.fetchall()


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
def get_max_datas(cursor: RealDictCursor, select, table_name: str) -> list:
    query = sql.SQL(
        '''
        SELECT MAX({select}) 
        FROM {table} ''').format(
        select=sql.Identifier(select),
        table = sql.Identifier(table_name))
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def delete(cursor: RealDictCursor, table_name: str, column_name: str, value) -> list:
    query = sql.SQL(
        '''
        DELETE FROM {table} 
        WHERE {table} = %s''').format(
        table=sql.Identifier(table_name),
        column = sql.Identifier(column_name))
    cursor.execute(query, [value])


@database_common.connection_handler
def update_where(cursor: RealDictCursor, table_name: str, set_name: str, set_value, column_name: str, where_value) -> list:
    query = sql.SQL(
        '''
        UPDATE {table}
        SET {set} = %s
        WHERE {column} = %s''').format(
        table=sql.Identifier(table_name),
        set=sql.Identifier(set_name),
        column = sql.Identifier(column_name))
    cursor.execute(query, [set_value, where_value])


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
def get_search_result_questions_id(cursor: RealDictCursor, phrase: str) -> list:
    query = """
    SELECT id
    FROM question
    WHERE title ilike %s OR message ilike %s
    """
    cursor.execute(query, ['%'+phrase+'%', '%'+phrase+'%'])
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
def add_new_user(cursor: RealDictCursor, username, hashed_password, date) -> list:
    query = """
    INSERT INTO users(name, password, created_date, reputation)
    VALUES (%s, %s, %s, 0)
    """
    cursor.execute(query, [username, hashed_password, date])


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
def update_user_data(cursor: RealDictCursor, title, message, image, question_id):
    query = """
    UPDATE question 
    SET title = %s, message = %s, image = %s 
    WHERE id = %s
            """
    cursor.execute(query, [title, message, image, question_id])


@database_common.connection_handler
def update_user_answer(cursor: RealDictCursor, message, image, answer_id) -> list:
    query = """
    UPDATE answer
    SET message = %s, image = %s
    WHERE id = %s
    """
    cursor.execute(query, [message, image, answer_id])


@database_common.connection_handler
def update_comment(cursor: RealDictCursor, update_comment, updated_date, edited_count,  comment_id) -> list:
    query = """
    UPDATE comment
    SET message = %s, submission_time = %s, edited_count = %s
    WHERE id = %s
    """
    cursor.execute(query, [update_comment, updated_date, edited_count, comment_id])


@database_common.connection_handler
def delete_tags(cursor: RealDictCursor, question_id, tag_id) -> list:
    query = """
    DELETE FROM question_tag
    WHERE question_id = %s AND tag_id = %s
    """
    cursor.execute(query, [question_id, tag_id])