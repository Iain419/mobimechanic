from base64 import b64encode
from datetime import timedelta
import flask
import html


from flask import Flask, render_template, request, redirect
import pymysql

app = Flask(__name__) #starting a flask app
# Set session exipiry lifetime if not in use
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)


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

# browse route
@app.route('/browse')
def browse():
    conn = pymysql.connect(
        host='localhost',
        user='root', 
        password = "",
        db='mobimechanic',
        )
    sql = 'SELECT * FROM `mechanics` WHERE `approve` = "yes"'
    cursor = conn.cursor()
    cursor.execute(sql)
    # Check the number of rows found
    if cursor.rowcount < 1:
            return render_template('browse.html')
    else:
        rows = cursor.fetchall()
        # return all rows the templates, in templates check if image is decoded to utf and base 64
        return render_template('browse.html', rows=rows)

@app.route('/registerm', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        # html.escape protects against XXS and SQL injection
        idno = int(request.form['idno'])
        firstname = str(request.form['firstname'])
        lastname = str(request.form['lastname'])
        phoneno = str(request.form['phoneno'])
        location = str(request.form['location'])
        areaofspecification = str(request.form['areaofspecification'])
        services = str(request.form['services'])
        ratings = str(request.form['ratings'])
        charge = str(request.form['charge'])
        email = str(request.form['email'])
        password = str(request.form['password'])
        photo = request.files["photo"]
        # read image
        readimage = photo.read()  # read the image file data, the real image
        # encode image to base64 and decode to utf-8
        encodedimage = b64encode(readimage).decode("utf-8")


        import re
        # check if passw match with  - password again(confirm)
        #  more validation on inputs can be done here, empties, length, range

        if password != password:
            return render_template('register.html', msg="Passwords do not match")

        # Check password strength, this stops brute force.
        elif (len(password) < 8):
            return render_template('register.html', msg="Password must have eight characters")

            # must have eigtht characters

        elif not re.search("[a-z]", password):
            return render_template('register.html', msg="Password must have small letters")

        elif not re.search("[A-Z]", password):
            return render_template('register.html', msg="Password must have a character with a capital letter")


        elif not re.search("[0-9]", password):
            return render_template('register.html', msg="Must have a number")

        elif not re.search("[!@#$%^&*()_]", password):
            return render_template('register.html', msg="Trial using symbols in your password e.g !@#$%^&*()")

        else:
            conn = pymysql.connect('localhost', 'root', '', 'propertydb')
            sql = 'INSERT INTO register (uname, email, passw, tel, Gender) VALUES (%s, %s, %s, %s, %s)'
            cursor = conn.cursor()
            # try:
            # password must be hashed, check how its provide below.
            # Its hashed, check hash function on line 48
            cursor.execute(sql, (uname, email, hash_password(passw), tel, Gender))
            conn.commit()
            return redirect('/login')

            # #except:
            #     return render_template('register.html', msg2="Registration Unsuccessful")

    else:
        return render_template('register-m.html')






# run
if __name__ == '__main__':
    app.run(debug=True, port=5000)
    print("App is running")
# port = 10000