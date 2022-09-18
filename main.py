from flask import Flask,render_template,request,redirect,session
import mysql.connector
from sentiment import second
import pickle
import os

# Defining Flask app
app =Flask(__name__)

app.secret_key=os.urandom(24)
app.register_blueprint(second)

#loading the trained ML model
emotion_pred_model = pickle.load(open('./models/emotion_pred_model.pkl','rb'))
try:
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="users")
    cursor=conn.cursor()
except:
    print("An exception occured")

@app.route('/')
def login():
    return render_template('signin.html')

@app.route('/register')
def register():
    return render_template('signin.html')

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('twitter.html')
    else:
        return redirect('/')


@app.route('/emotion')
def emotion_sentiment():
    return render_template('emotion.html')


@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.route('/about')
def about_us():
    return render_template('about.html')

@app.route('/Pie')
def pie():
    return render_template('Pie_chart.html')


@app.route('/login_validation', methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')

    cursor.execute("""SELECT * from `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email, password))
    users = cursor.fetchall()
    if len(users)>0:
        session['user_id']=users[0][0]
        return redirect('/home')
    else:
        return redirect('/')


@app.route('/add_user', methods=['POST'])
def add_user():
    name=request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')
    cursor.execute("""INSERT INTO `users` (`name`,`email`,`password`) VALUES ('{}','{}','{}')""".format(name,email, password))
    conn.commit()
    cursor.execute("""SELECT * from `users` WHERE `email` LIKE '{}'""".format(email))
    myuser=cursor.fetchall()
    session['user_id']=myuser[0][0]
    return redirect('/home')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')


@app.route('/emotion', methods=['GET','POST'])
def emotionanalysis():

    output = 'Result'
    if request.method == 'POST':
        keyword = request.form.get('emo_text')
        output = emotion_pred_model.predict([keyword])

        if output == 'joy':
            output = "Joy 😄"
        elif output =='neutral':
            output = "neutral 🙂"
        elif output =='sadness':
            output = "sadness 😔"
        elif output =='fear':
            output = "fear 😱"
        elif output =='surprise':
            output = "surprise 😃"
        elif output =='anger':
            output = "anger 😠"

    return render_template('emotion.html', prediction=f'{output}')



if __name__=="__main__":
    app.run(debug=True)