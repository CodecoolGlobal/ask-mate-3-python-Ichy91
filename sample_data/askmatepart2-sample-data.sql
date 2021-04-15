--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

ALTER TABLE IF EXISTS ONLY public.question DROP CONSTRAINT IF EXISTS pk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS pk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS pk_comment_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS pk_question_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.tag DROP CONSTRAINT IF EXISTS pk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS fk_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS pk_id CASCADE;


DROP TABLE IF EXISTS public.question;
CREATE TABLE question (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    view_number integer,
    vote_number integer,
    title text,
    message text,
    image text,
    user_id integer
);

DROP TABLE IF EXISTS public.answer;
CREATE TABLE answer (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    vote_number integer,
    question_id integer,
    message text,
    image text,
    user_id integer,
    accepted bool default FALSE
);

DROP TABLE IF EXISTS public.comment;
CREATE TABLE comment (
    id serial NOT NULL,
    question_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone,
    edited_count integer,
    user_id integer
);


DROP TABLE IF EXISTS public.question_tag;
CREATE TABLE question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);

DROP TABLE IF EXISTS public.tag;
CREATE TABLE tag (
    id serial NOT NULL,
    name text
);

DROP TABLE IF EXISTS public.users;
CREATE TABLE users (
    id serial NOT NULL,
    name text,
    password text,
    created_date timestamp without time zone,
    reputation integer
);


ALTER TABLE ONLY users
    ADD CONSTRAINT pk_id PRIMARY KEY (id);

ALTER TABLE ONLY answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);

ALTER TABLE ONLY question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);

ALTER TABLE ONLY tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES answer(id);

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES tag(id);


INSERT INTO question VALUES (1, '2017-04-28 08:29:00', 29, 7, 'How to make lists in Python?', 'I am totally new to this, any hints?', NULL, 1);
INSERT INTO question VALUES (2, '2017-04-29 09:19:00', 15, 9, 'Wordpress loading multiple jQuery Versions', 'I developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $(".myBook").booklet();

I could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine.

BUT in my theme i also using jquery via webpack so the loading order is now following:

jquery
booklet
app.js (bundled file with webpack, including jquery)', 'images/download1.png', 1);
INSERT INTO question VALUES (3, '2017-05-01 10:41:00', 1364, 57, 'Drawing canvas with an image picked with Cordova Camera Plugin', 'I''m getting an image from device and drawing a canvas with filters using Pixi JS. It works all well using computer to get an image. But when I''m on IOS, it throws errors such as cross origin issue, or that I''m trying to use an unknown format.
', NULL, 1);
INSERT INTO question VALUES(4,'2021-04-15 18:21:23', 14000, 13, 'Psycopg2 and SQL injection security', 'I am writing a class to be used as part of a much larger modeling algorithm. My part does spatial analysis to calculate distances from certain points to other points. There are a variety of conditions involving number of returned distances, cutoff distances, and etc.

Currently, the project specification only indicates hardcoded situations. i.e. "Function #1 needs to list all the distances from point set A to point set B within 500m. Function #2 needs to list all the distances from point set C to point set D..." and so on.

I don''t want to hardcode these parameters, and neither does the person who is developing the next stage of the model, because obviously they would like to tweak the parameters or possibly re-use the algorithm in other projects where they will have different conditions.

Now the problem is that I am using psycopg2 to do this. This is the standard where I work so I do not have a choice of deviating from it. I have read that it is a very bad idea to expose parameters that will be put into the executed queries as parameters due to the obvious reason of SQL injection. However, I thought that psycopg2 automatically sanitized SQL input. I think that the issue is using the AsIs function.

The easy solution is just to hardcode it as specified in the project but this feels lazy and sloppy to me. I don''t like doing lazy and sloppy work.

Is it at all safe to allow the user to input parameters that will be input into a psycopg2-executed query? Or is it just using AsIs that makes it unsafe? If I wanted to allow the user to be able to input these parameters, do I have to take the responsibility upon myself to santitize the inputs, and if so, is there a quick and easy way to do it, like with another python library or something?', NULL, 1);
INSERT INTO question VALUES(5,'2021-04-15 18:21:35', 745000, 981, 'Pg_config executable not found', 'Error: pg_config executable not found.

Please add the directory containing pg_config to the PATH

or specify the full executable path with the option:



    python setup.py build_ext --pg-config /path/to/pg_config build ...



or with the pg_config option in ''setup.cfg''.

----------------------------------------
Command python setup.py egg_info failed with error code 1 in /tmp/pip-build/psycopg2
But the problem is pg_config is actually in my PATH; it runs without any problem:

$ which pg_config
/usr/pgsql-9.1/bin/pg_config
I tried adding the pg_config path to the setup.cfg file and building it using the source files I downloaded from their website (http://initd.org/psycopg/) and I get the following error message!

Error: Unable to find ''pg_config'' file in ''/usr/pgsql-9.1/bin/''
But it is actually THERE!!!

I am baffled by these errors. Can anyone help please?

By the way, I sudo all the commands. Also I am on RHEL 5.5.
', NULL, 1);
INSERT INTO question VALUES(6,'2021-04-15 18:22:18', 423000, 555, 'How to install psycopg2 with “pip” on Python?', 'I''m using virtualenv and I need to install "psycopg2".

I have done the following:

pip install http://pypi.python.org/packages/source/p/psycopg2/psycopg2-2.4.tar.gz#md5=24f4368e2cfdc1a2b03282ddda814160
And I have the following messages:

Downloading/unpacking http://pypi.python.org/packages/source/p/psycopg2/psycopg2
-2.4.tar.gz#md5=24f4368e2cfdc1a2b03282ddda814160
  Downloading psycopg2-2.4.tar.gz (607Kb): 607Kb downloaded
  Running setup.py egg_info for package from http://pypi.python.org/packages/sou
rce/p/psycopg2/psycopg2-2.4.tar.gz#md5=24f4368e2cfdc1a2b03282ddda814160
    Error: pg_config executable not found.

    Please add the directory containing pg_config to the PATH
    or specify the full executable path with the option:

        python setup.py build_ext --pg-config /path/to/pg_config build ...

    or with the pg_config option in ''setup.cfg''.
    Complete output from command python setup.py egg_info:
    running egg_info

creating pip-egg-info\psycopg2.egg-info

writing pip-egg-info\psycopg2.egg-info\PKG-INFO

writing top-level names to pip-egg-info\psycopg2.egg-info\top_level.txt

writing dependency_links to pip-egg-info\psycopg2.egg-info\dependency_links.txt

writing manifest file ''pip-egg-info\psycopg2.egg-info\SOURCES.txt''

warning: manifest_maker: standard file ''-c'' not found

Error: pg_config executable not found.



Please add the directory containing pg_config to the PATH

or specify the full executable path with the option:



    python setup.py build_ext --pg-config /path/to/pg_config build ...



or with the pg_config option in ''setup.cfg''.

----------------------------------------
Command python setup.py egg_info failed with error code 1
Storing complete log in C:\Documents and Settings\anlopes\Application Data\pip\p
ip.log
My question, I only need to do this to get the psycopg2 working?

python setup.py build_ext --pg-config /path/to/pg_config build ...', NULL, 1);
SELECT pg_catalog.setval('question_id_seq', 6, true);

INSERT INTO answer VALUES (1, '2017-04-28 16:49:00', 4, 1, 'You need to use brackets: my_list = []', NULL, 2);
INSERT INTO answer VALUES (2, '2017-04-25 14:42:00', 0, 1, 'Look it up in the Python docs', 'images/questionmark.jpeg', 2);
INSERT INTO answer VALUES (3, '2021-04-15 18:25:11', 25, 4, 'You can use psycopg2.sql to compose dynamic queries. Unlike AsIs it will protect you from SQL injection.',NULL, 2);
INSERT INTO answer VALUES (4, '2021-04-15 18:26:55', 25, 4, 'AsIs is unsafe, unless you really know what you are doing. You can use it for unit testing for example.

Passing parameters is not that unsafe, as long as you do not pre-format your sql query. Never do:

sql_query = ''SELECT * FROM {}''.format(user_input)
cur.execute(sql_query)
Since user_input could be '';DROP DATABASE;'' for instance.

Instead, do:

sql_query = ''SELECT * FROM %s''
cur.execute(sql_query, (user_input,))
pyscopg2 will sanitize your query. Also, you can pre-sanitize the parameters in your code with your own logic, if you really do not trust your user''s input.

Per psycopg2''s documentation:

Warning Never, never, NEVER use Python string concatenation (+) or string parameters interpolation (%) to pass variables to a SQL query string. Not even at gunpoint.

Also, I would never, ever, let my users tell me which table I should query. Your app''s logic (or routes) should tell you that.

Regarding AsIs(), per psycopg2''s documentation :

Asis()... for objects whose string representation is already valid as SQL representation.

So, don''t use it with user''s input.',NULL, 2);
INSERT INTO answer VALUES(5,'2021-04-15 18:33:33', 9, 5, 'Simply run the following: sudo apt install libpq-dev Fixed the issue for me',NULL, 2);
INSERT INTO answer VALUES(6,'2021-04-15 18:33:33', 913, 6, 'Note: Since a while back, there are binary wheels for Windows in PyPI, so this should no longer be an issue for Windows users. Below are solutions for Linux, Mac users, since lots of them find this post through web searches.

Option 1
Install the psycopg2-binary PyPI package instead, it has Python wheels for Linux and Mac OS.

pip install psycopg2-binary
Option 2
Install the prerequsisites for building the psycopg2 package from source:

Debian/Ubuntu
Python 3
sudo apt install libpq-dev python3-dev
You might need to install python3.8-dev or similar for e.g. Python 3.8.

Python 21
sudo apt install libpq-dev python-dev
If that''s not enough, try

sudo apt install build-essential
or

sudo apt install postgresql-server-dev-all
as well before installing psycopg2 again.

CentOS 6
See Banjer''s answer',NULL ,2);
SELECT pg_catalog.setval('answer_id_seq', 6, true);

INSERT INTO comment VALUES (1, 1, NULL, 'Please clarify the question as it is too vague!', '2017-05-01 05:49:00', 0, 3);
INSERT INTO comment VALUES (2, NULL, 1, 'I think you could use my_list = list() as well.', '2017-05-02 16:55:00', 0, 3);
INSERT INTO comment VALUES (3, NULL, 4, 'So the main takeaway is: Do not use AsIs(). Are there any restrictions for things like setting table names? I seem to recall reading somewhere that you can input values via the execute() command, but you shouldn''t use it in table names. Does this sound right or am I completely off? And yes, I never use string concatenation, nor string parameters/formatting. But I was a little confused because I was starting to think that even using the execute() command was also unsafe, which was starting make me wonder what the whole point of the library was', '2021-04-15 16:28:14', 0, 3);
SELECT pg_catalog.setval('comment_id_seq', 3, true);

INSERT INTO tag VALUES (1, 'python');
INSERT INTO tag VALUES (2, 'sql');
INSERT INTO tag VALUES (3, 'css');
SELECT pg_catalog.setval('tag_id_seq', 3, true);

INSERT INTO question_tag VALUES (1, 1);
INSERT INTO question_tag VALUES (2, 3);
INSERT INTO question_tag VALUES (3, 3);

INSERT INTO users VALUES (1,'test','$2b$12$vbodl658tstz1yXMOmqgR.NAPIX76GYhLB6PMhaEojn2OZ79Lg0JS','2017-04-11 17:11:32', 0);
INSERT INTO users VALUES (2,'asker','$2b$12$R23TY59Dp5it7XXnNzdXx.178XtxLECKG5MRhZKGXgjfFRuWANV8.','2017-04-11 14:42:00', 0);
INSERT INTO users VALUES (3,'commenter', '$2b$12$XcT3utYd79YToMKeIh86RuU.29B/Qt/f0.KrtYT7DIFCbTW2IehtW','2017-04-11 18:19:11', 0);
SELECT pg_catalog.setval('users_id_seq', 3, true);
