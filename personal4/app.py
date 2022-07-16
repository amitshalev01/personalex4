import random
from flask import Flask, redirect, url_for
from flask import render_template
from datetime import timedelta
from flask import request, session, jsonify
import mysql.connector
import time
from pages.assignment_4.assignment_4 import assignment_4


app = Flask(__name__)
app.register_blueprint(assignment_4)
app.secret_key = '123'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)


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













@app.route('/')
def home_page():
    return render_template('homepage.html')

@app.route('/base')
def base_page():
    return render_template('base.html')

@app.route('/contact')
def contact_page():
    return render_template('contact.html')

@app.route('/assignment3_1')
def assignment3_1_page():
    user = {'first_name': 'AmIT', 'last_name': 'sHAlEv', 'phone_number': '05222222222', 'email': 'amitsh@gmail.com',
            'Nationallity': 'IsRaelI'}
    hobbies = ['plAyInG basKEtball', 'reading books', 'TRaveling', 'traveling', 'sailing', 'watch comedies']
    movies_dictionary = {'Comedies': ['jump st.', 'the trip', 'THE TRIP', 'meet the parents'],
                                 'ACTiOn': ['fast & furious', 'jango', 'save ryan'],
                                 'DraMa': ['belfast', '365 days', 'hasandak', 'belfast', 'strange things'],
                                 'bUrekas': ['Charlie and a half', 'hagiga ba snooker', 'ALex HOLE ahava']}
    topMovie = 'Belfast'
    session['topMovie'] = topMovie

    # the values includes duplicates and errors in order to see if the filters are working
    return render_template('assignment3_1.html',
                           user=user,
                           hobbies=hobbies,
                           movies_dictionary=movies_dictionary,
                           topMovie=topMovie)

users = {
        'user1': {'user_name': 'Amit', 'user_id': '324567876', 'user_email': 'amits@gmail.com', 'user_password': 'sdrrAws23','user_age': '25'},
        'user2': {'user_name': 'Tal', 'user_id': '456722123', 'user_email': 'talcod@gmail.com', 'user_password': 'gtyf5XC4t','user_age': '33'},
        'user3': {'user_name': 'Ben', 'user_id': '213432128', 'user_email': 'benben@gmail.com', 'user_password': 'fgddhj433','user_age': '23'},
        'user4': {'user_name': 'Romi', 'user_id': '788444555', 'user_email': 'ftromi@gmail.com', 'user_password': 'eZweec46y','user_age': '57'},
        'user5': {'user_name': 'Yossi', 'user_id': '111222333', 'user_email': 'yossilev@gmail.com','user_password': 'ghgh22Q','user_age': '41'},
    }

@app.route('/assignment3_2', methods=['GET', 'POST'])
def assignment3_2_page():
    if request.method == 'GET':
        finduser = False
        if 'user_id' in request.args:
                if request.args['user_id'] =='':
                    return render_template('assignment3_2.html',
                                users=users)
                else:
                    for spe_user_id, user_dic in users.items():
                            for k in user_dic:
                                if k =='user_id':
                                  if (user_dic[k] == request.args[k]):
                                    finduser=True
                                    user_name = user_dic['user_name']
                                    user_ID = user_dic['user_id']
                                    user_email = user_dic['user_email']
                                    user_password=user_dic['user_password']
                                    user_age = user_dic['user_age']

                                    return render_template('assignment3_2.html',
                                                           user_name=user_name,
                                                           user_ID=user_ID,
                                                           user_email=user_email,
                                                           user_password=user_password,
                                                           user_age=user_age,
                                                           )
                    if finduser == False:
                        return render_template('assignment3_2.html',
                                               message='user not found.')
    elif request.method == 'POST':
            user_name = request.form['user_name']
            user_id = request.form['user_id']
            user_email = request.form['user_email']
            user_password = request.form['user_password']
            user_age = request.form['user_age']

            for spe_user_id, user_dic in users.items():
                for key in user_dic:
                    if key == 'user_id':
                        if user_dic[key] == user_id:
                            return render_template('assignment3_2.html',
                                                   register_display_massage='this ID already exists in our system ')


            session['username_new'] = user_name
            session['registered'] = True
            newUserInfo = {'user_name': user_name,  'user_id': user_id, 'user_email': user_email, 'user_password': user_password, 'user_age': user_age}
            users['user' + str((len(users.keys())+1))] = newUserInfo
            return render_template('assignment3_2.html',
                                   register_display_massage='Success',
                                            username_new=user_name)

    return render_template('assignment3_2.html')

@app.route('/logout')
def logout_page():
    session['registered'] = False
    session.clear()
    return redirect(url_for('assignment3_2_page'))

@app.route('/top_movie')
def top_movie_function():
    return redirect("https://en.wikipedia.org/wiki/" + session['topMovie']+"_(film)")


if __name__ == '__main__':
    app.run(debug=True)
