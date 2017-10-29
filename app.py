#.............................................
# importing files
#..............................................

from flask import request, Flask,render_template, flash,redirect,url_for,session,logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField,PasswordField, validators
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
    return render_template('home.html')

#..............................................
#about route
#..............................................


@app.route('/about')
def about():
    return render_template('about.html')


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





if __name__ =='__main__':
    app.secret_key= 'secret123'
    app.run(debug =True)
