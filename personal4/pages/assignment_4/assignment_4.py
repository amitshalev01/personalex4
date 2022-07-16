from flask import render_template, Blueprint, request, redirect, jsonify, url_for, session
import requests
from flask import flash
import app
import mysql
assignment_4 = Blueprint('assignment_4', __name__,
                         static_folder='static',
                         static_url_path='/assignment_4',
                         template_folder='templates')

@assignment_4.route('/assignment_4')
def assignment_4_page():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    return render_template('assignment4.html', users=users_list)


def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         passwd='root',
                                         database='assignment4')
    cursor = connection.cursor(named_tuple=True)
    cursor.execute(query)
    #

    if query_type == 'commit':
        # Use for INSERT, UPDATE, DELETE statements.
        # Returns: The number of rows affected by the query (a non-negative int).
        connection.commit()
        return_value = True

    if query_type == 'fetch':
        # Use for SELECT statement.
        # Returns: False if the query failed, or the result of the query if it succeeded.
        query_result = cursor.fetchall()
        return_value = query_result

    connection.close()
    cursor.close()
    return return_value

# ------------------------------------------------- #
# ------------------- SELECT ---------------------- #
# ------------------------------------------------- #
@assignment_4.route('/users')
def users():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    return render_template('assignment4.html', users=users_list)


# ------------------------------------------------- #
# ------------------------------------------------- #


# ------------------------------------------------- #
# -------------------- INSERT --------------------- #
# ------------------------------------------------- #
@assignment_4.route('/insert_user', methods=['POST'])
def insert_user():
    name = request.form['user_name']
    id = request.form['user_id']
    email = request.form['user_email']
    password = request.form['user_password']
    age = request.form['user_age']
    print(f'{name} {id} {email} {password} {age}')
    if find_user(id):
        flash("User with this ID is already existing")
        return redirect('/assignment_4')
    query = "INSERT INTO users(user_name, user_ID, user_email, user_password, user_age) VALUES ('%s', '%s', '%s' , '%s' , '%s')" % (name, id, email, password, age)
    interact_db(query=query, query_type='commit')
    return redirect('/assignment_4')

@assignment_4.route('/delete_user', methods=['POST'])
def delete_user_func():
    user_id = request.form['user_id_delete']
    if not find_user(user_id):
        flash("User is not existing")
        return redirect('/assignment_4')
    else:
        query = "DELETE FROM users WHERE user_ID='%s';" % user_id
        # print(query)
        interact_db(query, query_type='commit')
        return redirect('/assignment_4')


def find_user(num):
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    print(users_list)
    for i in users_list:
        if i.user_ID == num:
            return True
    return False

@assignment_4.route('/update_user', methods=['POST'])
def update_user_func():
    id = request.form['user_id']
    if not find_user(id):
        flash("User with this ID is not existing")
        return redirect('/assignment_4')
    if request.form['user_name'] != '':
        name = request.form['user_name']
        query = "UPDATE users SET user_name='%s'  WHERE user_id='%s' ;" % (name, id)
        interact_db(query, query_type='commit')
    if request.form['user_email'] != '':
       email = request.form['user_email']
       query = "UPDATE users SET  user_email='%s'  WHERE user_id='%s' ;" % (email, id)
       interact_db(query, query_type='commit')
    if request.form['user_password'] != '':
       password = request.form['user_password']
       query = "UPDATE users SET  user_password='%s'  WHERE user_id='%s' ;" % (password , id)
       interact_db(query, query_type='commit')
    if request.form['user_age'] != '':
       age = request.form['user_age']
       query = "UPDATE users SET  user_age='%s'  WHERE user_id='%s' ;" % (age , id)
       interact_db(query, query_type='commit')

    flash("user updated successfully")
    return redirect('/assignment_4')

@assignment_4.route('/assignment_4/users')
def json_users_table_func():
    query = 'select * from users'
    users_list = app.interact_db(query, query_type='fetch')
    return jsonify(users_list)

@assignment_4.route('/assignment4_outer_source')
def assignment4_outer_source_page():
    return render_template('assignment4_outer_source.html')

@assignment_4.route('/fetch_back_end')
def fetch_back_end_func():
    inputID = request.args['id_backend']
    userRes= requests.get(f'https://reqres.in/api/users/{inputID}')
    userData=userRes.json()
    for userData_Key, userData_Values in userData.items():
        for key in userData_Values:
            if key == 'avatar':
                picture = userData_Values['avatar']
            if key == 'first_name':
                userFirstName=userData_Values['first_name']
            if key == 'last_name':
                userLastName = userData_Values['last_name']
            if key == 'email':
             userEmail = userData_Values['email']

    return render_template('assignment4_outer_source.html', userFirstName=userFirstName
                           , userLastName=userLastName, picture=picture, userEmail=userEmail)

@assignment_4.route('/assignment4/restapi_users', defaults={'user_ID': 324567876})
@assignment_4.route('/assignment4/restapi_users/<int:user_ID>')
def restapi_users__func(user_ID):
    if user_ID == 324567876:
        default_query = "select * FROM users WHERE user_ID='324567876';"
        users_list = app.interact_db(default_query, query_type='fetch')
        default_response = users_list[0]
        default_response = jsonify(default_response)
        return default_response


    user_query = "select * FROM users WHERE user_ID='%s';" % user_ID
    users_list = app.interact_db(user_query, query_type='fetch')

    if len(users_list) != 0:
        user_response = users_list[0]
    else:
        user_response={
        'error':'User is not found'
        }
    user_response = jsonify(user_response)
    return user_response
