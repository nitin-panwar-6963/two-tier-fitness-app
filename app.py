from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.secret_key = os.getenv('SECRET_KEY')

mysql = MySQL(app)
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('login.html')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                    (username, email, password))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    return render_template('register.html')

# Login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password_input = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username=%s", [username])
    user = cur.fetchone()
    cur.close()

    if user and bcrypt.check_password_hash(user[3], password_input):
        session['user_id'] = user[0]
        session['username'] = user[1]
        return redirect('/dashboard')
    else:
        return "Invalid Credentials. <a href='/'>Try again</a>"

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('dashboard.html', username=session['username'])

@app.route('/exercises', methods=['GET', 'POST'])
def exercises():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        description = request.form['description']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO exercises (name, category, description) VALUES (%s,%s,%s)",
                    (name, category, description))
        mysql.connection.commit()
        cur.close()
        return redirect('/exercises')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM exercises")
    data = cur.fetchall()
    cur.close()
    return render_template('exercises.html', exercises=data)

@app.route('/workouts', methods=['GET', 'POST'])
def workouts():
    if 'user_id' not in session:
        return redirect('/')
    
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        exercise_id = request.form['exercise_id']
        date = request.form['date']
        reps = request.form['reps']
        sets = request.form['sets']
        cur.execute("INSERT INTO workouts (user_id, exercise_id, date, reps, sets) VALUES (%s,%s,%s,%s,%s)",
                    (session['user_id'], exercise_id, date, reps, sets))
        mysql.connection.commit()

    cur.execute("""SELECT w.id, e.name, w.date, w.reps, w.sets
                   FROM workouts w JOIN exercises e ON w.exercise_id=e.id
                   WHERE w.user_id=%s""", [session['user_id']])
    data = cur.fetchall()

    cur.execute("SELECT * FROM exercises")
    exercises = cur.fetchall()
    cur.close()
    return render_template('workouts.html', workouts=data, exercises=exercises)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0' , port=5000)

