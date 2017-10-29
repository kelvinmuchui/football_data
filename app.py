#.............................................
# importing files
#..............................................

from flask import request, Flask,render_template, flash,redirect,url_for,session,logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField,PasswordField, IntegerField, validators
from passlib.hash import sha256_crypt
from functools import wraps



#app config

app = Flask(__name__)

#...........................................................................
                #config MySQL
#................................................................................
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'datahouse'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


    #init MYSQL_DB
mysql = MySQL(app)




#........................................
#home routues
#........................................

@app.route('/')
def index():
        #create cursor
    cur = mysql.connection.cursor()


    #Get articles
    result = cur.execute("SELECT * FROM teams")
    teams = cur.fetchall()

    if result >0:
        return render_template('home.html', teams=teams)
    else:
        msg = 'No teams Found'
        return render_template('dashboard.html', msg =msg)

    #close connection
    cur.close()
    return render_template('home.html')

#..............................................
#about route
#..............................................


@app.route('/about')
def about():
    return render_template('about.html')

#..............................................
#teams route
#...............................................

@app.route('/teams')
def teams():
    #create curser
    cur = mysql.connection.cursor()


    #Get teams
    result = cur.execute("SELECT * FROM teams")
    teams = curl.fetchall()

    if result > 0:
        return render_template('teams.html')
    else:
        msg = "No Teams  Found"
        return render_template('teams.html')

    #close connection
    cur.close()

#..............................................
#team route
#..............................................
@app.route('/team/<string:id>/')
def team(id):


    #create cursor
    cur = mysql.connection.cursor()


    #get team
    result = cur.execute("SELECT * FROM teams WHERE id = %s ", [id])
    team = cur.fetchone()

    return render_template('team.html', team=team)



#..............................................
#registration Form
#...............................................

class RegisterForm(Form):
    username = StringField('Username',[validators.Length(min=4, max = 15)])
    email = StringField('Email', [validators.Length(min = 5, max =30)])
    password = PasswordField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Password doesnot match')
        ])
    confirm = PasswordField('Confirm Password')

#...............................................................
#register route
#...............................................................

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))

        #creaate cursor

        cur = mysql.connection.cursor()


        cur.execute('INSERT INTO users(username, email, password) VALUES(%s, %s, %s)', (username, email, password))

        #Commit to db

        mysql.connection.commit()

        #Close connection

        cur.close()


        flash('You are now registered can can login', 'success')


        return redirect(url_for('index'))

        return render_template('register.html', form = form)
    return render_template('register.html', form = form)


#.......................................................................
#user login
#.......................................................................

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        #get form fields
        username = request.form['username']
        password_candidate = request.form['password']


        #create cursor
        cur = mysql.connection.cursor()


        #get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s",[username])
        if result > 0:
            #get stored hash
            data = cur.fetchone()
            password = data ['password']


            #compare the password
            if sha256_crypt.verify(password_candidate, password):
                #Passed
                session['logged_in'] =True
                session ['username'] = username

                flash ('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = "Invalid Login"
                return render_template('login.html', error=error)
            #close connection
            cur.close()
        else:
            error = "Username not found"
            return render_template('login.html', error = error)
    return render_template('login.html')

#.........................................................
#Check if user is logged in
#.........................................................


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', "danger")
            return redirect(url_for('login'))
    return wrap

    #...........................................
    #dashboard
    #.............................................
@app.route('/dashboard')
@is_logged_in
def dashboard():
        #create cursor
    cur = mysql.connection.cursor()


    #Get articles
    result = cur.execute("SELECT * FROM teams")
    teams = cur.fetchall()

    if result >0:
        return render_template('dashboard.html', teams=teams)
    else:
        msg = 'No teams Found'
        return render_template('dashboard.html', msg =msg)

    #close connection
    cur.close()
class TeamForm(Form):
    name = StringField('Name', [validators.Length(min =1, max =200)])
    history = TextAreaField('History',[validators.Length(min =4)])
    homeground = StringField('Home Ground',[validators.Length(min =1, max =200)])
    trophy = IntegerField('Trophy')



#...............................................................................
            # add Article
#...............................................................................
@app.route('/add_team' ,methods =['GET', 'POST'])
@is_logged_in
def add_team():
    form =TeamForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        history = form.history.data
        homeground = form.homeground.data
        trophy = form.trophy.data

        #Create cursor

        cur  =mysql.connection.cursor()

        #execute
        cur.execute('INSERT INTO teams(name, history, homeground, trophy) VALUES(%s,%s,%s, %s)', (name, history, homeground, trophy))

        #Commit to Db
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('Team created', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_team.html', form=form)
#...............................................................................
                #logout
#...............................................................................
@app.route('/logout')
def logout ():
    session.clear()
    flash('you are now logged out', 'success')
    return redirect(url_for('login'))



if __name__ =='__main__':
    app.secret_key= 'secret123'
    app.run(debug =True)
