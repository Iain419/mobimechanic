from base64 import b64encode
from datetime import timedelta
import html


from flask import Flask, render_template, request, redirect, session
import pymysql

app = Flask(__name__) #starting a flask app
# Set session exipiry lifetime if not in use
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

app.secret_key = 'opoojm_5#y2L"F4Q8z\n\xec]/'


# activate HTTP only/secure to true
# activate samesite to 'Lax'
# This reduce chances of a Sessions Fixation/Hijacking

app.config.update(
    SESSION_COOKIE_SECURE=False,  # For it to work locally
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
)
# Home page route
@app.route('/')
def index():
    return render_template('index.html')



@app.route('/loginu', methods=['POST', 'GET'])
def loginu():
    if request.method == 'POST':
        username = str(request.form['username'])
        passw = str(request.form['passw']) 
        conn = pymysql.connect(
            host='localhost',
            user='root', 
            password = "",
            db='mobimechanic',
            )
        sql = "Select * from user where username=%s AND Password = %s"
        name = "SELECT `Firstname` FROM `user` WHERE `username` = %s AND `Password` = %s"
        cursor = conn.cursor()  # execute sql
        cursor.execute(sql, (username,passw))
        cursor2 = conn.cursor()
        cursor2.execute(name, (username,passw))
        name = cursor2.fetchone()
        

        if cursor.rowcount == 0:
            return render_template('login-u.html', msg='Login failed, Wrong password or Username')

        elif cursor.rowcount == 1:
                session['username'] =   username;
                session.permanent = True
                return render_template('filter.html')


    else:
        return render_template('login-u.html')

@app.route('/loginm', methods=['POST', 'GET'])
def loginm():
    if request.method == 'POST':
        username = str(request.form['username'])
        passw = str(request.form['passw']) 
        conn = pymysql.connect(
            host='localhost',
            user='root', 
            password = "",
            db='mobimechanic',
            )
        sql = "Select * from mechanics where username=%s AND Password = %s"
        name = "SELECT `Firstname` FROM `mechanics` WHERE `username` = %s AND `Password` = %s"
        cursor = conn.cursor()  # execute sql
        cursor.execute(sql, (username,passw))
        cursor2 = conn.cursor()
        cursor2.execute(name, (username,passw))
        name = cursor2.fetchone()
        

        if cursor.rowcount == 0:
            return render_template('login-m.html', msg='Login failed, Wrong password or Username')

        elif cursor.rowcount == 1:
                session['username'] =   username;
                session.permanent = True
                return render_template('filter.html')


    else:
        return render_template('login-m.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('filter.html')

# filter
@app.route('/filter', methods=['POST', 'GET'])
def filter():
    if request.method == 'POST':
        location = str(request.form['location'])
        problem = str(request.form['problem'])
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password = "",
            db='mobimechanic'
        )
        sql = 'SELECT * FROM `mechanics` WHERE `approve` = 1 AND location = %s AND areaofspecification = %s'
        cursor = conn.cursor()
        cursor.execute(sql, (location,problem))
        # Check the number of rows found
        if cursor.rowcount < 1:
                return render_template('filter.html', msg="Sorry we could not find you a mechanic")
        else:
            rows = cursor.fetchall()
            return render_template('browse.html', rows=rows)
    else:
        return redirect('/')


# browse route
@app.route('/browse')
def browse():
    return render_template('filter.html')

@app.route('/registerm', methods=['POST', 'GET'])
def registerm():
    if request.method == 'POST':
        firstname = str(request.form['firstname'])
        lastname = str(request.form['lastname'])
        username = str(request.form['username'])
        email = str(request.form['email'])
        phoneno = str(request.form['phoneno'])
        password = str(request.form['password'])
        pass_again = str(request.form['pass_again'])
        idno = int(request.form['idno'])
        location = str(request.form['location'])
        charge = int(request.form['charge'])
        areaofspecification = str(request.form['areaofspecification'])
        photo = request.files["photo"]
        # read image
        readimage = photo.read()  # read the image file data, the real image
        # encode image to base64 and decode to utf-8
        encodedimage = b64encode(readimage).decode("utf-8")


        import re
        # check if passw match with  - password again(confirm)
        #  more validation on inputs can be done here, empties, length, range

        if password != pass_again:
            return render_template('register-m.html', msg="Passwords do not match")
        else:
            conn = pymysql.connect(
            host='localhost',
            user='root', 
            password = "",
            db='mobimechanic',
            )
            sql = "INSERT INTO `mechanics`(`Id_no`, `Firstname`, `Lastname`, `username`, `phoneno`, `location`, `areaofspecification`,`charge`, `email`, `password`, `photo`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor = conn.cursor()
            cursor.execute(sql, (idno, firstname, lastname, username, phoneno, location, areaofspecification, charge, email, password, encodedimage))
            conn.commit()
            return redirect('/')

            

    else:
        return render_template('register-m.html')


@app.route('/registeru', methods=['POST', 'GET'])
def registeru():
    if request.method == 'POST':
        firstname = str(request.form['firstname'])
        lastname = str(request.form['lastname'])
        username = str(request.form['username'])
        phoneno = int(request.form['phoneno'])
        email = str(request.form['email'])
        password = str(request.form['password'])
        pass_again = str(request.form['pass_again'])
        photo = request.files["photo"]
        # read image
        readimage = photo.read()  # read the image file data, the real image
        # encode image to base64 and decode to utf-8
        encodedimage = b64encode(readimage).decode("utf-8")
        

        if password != pass_again:
            return render_template('register-u.html', msg="Passwords do not match")
        else:
            conn = pymysql.connect(
            host='localhost',
            user='root', 
            password = "",
            db='mobimechanic',
            )
            sql = "INSERT INTO `user`(`Firstname`, `Lastname`, `username`, `phoneno`, `Email`, `Password`) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor = conn.cursor()
            cursor.execute(sql, (firstname, lastname, username, phoneno, email, password))
            conn.commit()
            return redirect('/loginu')
    else:
        return render_template('register-u.html')

# @app.route('/hire', methods=['GET', 'POST'])
# def hire():
#     product = Product.query.filter(Product.id == product_id)
#     cart_item = CartItem(product=product)
#     db.session.add(cart_item)
#     db.session.commit()

#     return render_tempate('home.html', product=products)




# run
if __name__ == '__main__':
    app.run(debug=True, port=5000)
# port = 10000