from flask import Flask, render_template, url_for, redirect, request, session, flash
from pymongo import MongoClient # import the pymongo
from bson.objectid import ObjectId #import this to convert ObjectID from string to it's datatype in MongoDB
import functools
import bcrypt # to encrypt password
import os
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename # for secure name
from datetime import datetime #datetime

client = MongoClient("mongodb://localhost:27017/") # connect on the "localhost" host and port 27017
db = client["astro"] # use/create "webapp" database
user_info = db.user
stars_content = db.stars_content
animals_content = db.animal_content
projects = db.project



# Create the Flask application
app = Flask(__name__)

# session secret_key
app.secret_key = 'fad62b7c1a6a9e67dbb66c3571a23ff2425650965f80047ea2fadce543b088cf'


# route here
@app.route('/')
def index():
    return render_template("home.html")

@app.route('/map')
def map():
    return render_template("map.html")

@app.route('/weather')
def weather():
    return render_template("weather.html")

@app.route('/schedule')
def schedule():
    all_projects = projects.find() # get all projects data
    all_projects_list = list(all_projects) # convert the data into list
    print(all_projects_list)
    return render_template("schedule.html", data=all_projects_list)



@app.route('/scheduledetail/<id>')
def schedule_Detail(id):
    # Convert from string to ObjectId:
    _id_converted = ObjectId(id)
    search_filter = {"_id": _id_converted} # _id is key and _id_converted is the converted _id
    project_data = projects.find_one(search_filter) # get one project data matched with _id
    
    return render_template("scheduledetail.html", data=project_data)

@app.route('/stars')
def stars():
    data = stars_content.find({"animal": "사수자리"})
    idx = datetime.today().day % 4
    content = []
    cnt = 0

    for el in data:
        if datetime.today().day % 4 == cnt:
            content.append(el['content'])
        
        cnt += 1


    return render_template('starpage.html', data=content)
    


@app.route('/mypage')
def mypage():
    if session.get('user_email'):
        # _id_converted = ObjectId(id)
        # search_filter = {"_id": _id_converted}
        # userData = user_info.find_one(search_filter)
        userData = user_info.find_one({"email": session.get('user_email')})
        star_content = find_star_content(userData['star']) # 유저의 별자리에 맞는 내용 반환.
        animal_content = find_animal_content(userData['animal'])
        return render_template("mypage.html", userData=userData, star_content=star_content[0], animal_content=animal_content[0], animal_icon = "fa-dragon")
    else:
        # if logged in
        user_email = session.get('user_email')
        login_email = user_info.find_one({"email": user_email})
        if login_email:
            return redirect(url_for('mypage', id=login_email['_id']))

        return redirect('/')
        # not logged in

    # _id_converted = ObjectId(id)
    #     search_filter = {"_id": _id_converted}
    #     userData = user_info.find_one(search_filter)
    #     return render_template("mypage.html", userData=userData)

@app.route('/searchMyLucky', methods=['GET', 'POST'])
def search_my_lucky():
    if request.method == 'POST':
        search_form = request.form['search_data']
        name, birth_day = search_form.split('/')
        animal, star = find_temporary_user_data(birth_day) # 생년월일에따른 별자리와 띠 찾아주는 함수
        star_content = find_star_content(star) # 별자리에 맞는 운세 반횐
        animal_content = find_animal_content(animal) # 띠에 맞는 운세 반환
        print(animal, star)

    return render_template("mylucky.html", name_data=name, birth_data=birth_day, animal=animal, star=star, star_content=star_content[0], animal_content=animal_content[0])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()


        is_member_email = user_info.find_one({"email": email})

        if is_member_email:
            member_password = is_member_email['password']
            if password == str(member_password):
                session['user_email'] = email
                print(is_member_email['_id'])
                # return redirect(url_for('mypage', id=is_member_email['_id']))
                return redirect(url_for('mypage'))
        
        else:
            return redirect(url_for('login'))
    
    user_email = session.get('user_email')
    if user_email:
        login_email = user_info.find_one({"email": user_email})
        # return redirect(url_for('mypage', id=login_email['_id']))
        return redirect(url_for('mypage'))
            

    return render_template("login.html")





@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# 별자리에 맞는 오늘의 운세 반환하는 함수.
def find_star_content(star):
    data = stars_content.find({"animal": star})
    idx = datetime.today().day % 4
    content = []
    cnt = 0
    for el in data:
        if datetime.today().day % 4 == cnt:
            content.append(el['content'])
        cnt += 1
    
    return content

def find_animal_content(animal):
    data = animals_content.find({"animal": animal})
    idx = datetime.today().day % 4
    content = []
    cnt = 0
    for el in data:
        if datetime.today().day % 4 == cnt:
            content.append(el['content'])
        cnt += 1
    
    return content


def find_temporary_user_data(birth_day):
    year, month, day = birth_day.split('.')
    year = int(year)
    month = int(month)
    day = int(day)
    tmp_animal = find_animal(year)
    tmp_star = find_stars(month, day)

    return [tmp_animal, tmp_star]

def find_animal(year):  
    animal_list = ['원숭이', '닭', '개', '돼지', '쥐', '소', '호랑이', '토끼', '용', '뱀', '말', '양']

    return animal_list[year % 12]

def find_stars(month, day):
    date = month * 100 + day

    if 120 <= date <= 218:
        return "물병자리"
    elif 219 <= date <= 320:
        return "물고기자리"
    elif 321 <= date <= 419:
        return "양자리"
    elif 420 <= date <= 520:
        return "황소자리"
    elif 521 <= date <= 621:
        return "쌍둥이자리"
    elif 622 <= date <= 722:
        return "게자리"
    elif 723 <= date <= 822:
        return "사자자리"
    elif 823 <= date <= 923:
        return "처녀자리"
    elif 924 <= date <= 1022:
        return "천칭자리"
    elif 1023 <= date <= 1122:
        return "전갈자리"
    elif 1123 <= date <= 1224:
        return "사수자리"
    else:
        return "염소자리"

# put the following code at the end of 'app.py' script
if __name__ == '__main__':
    app.run(debug=True) #debug is True, default host and port is 127.0.0.1:5000