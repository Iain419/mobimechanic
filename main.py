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
    sql = 'SELECT * FROM `mechanics` WHERE `approve` = 1'
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
        firstname = str(request.form['firstname'])
        lastname = str(request.form['lastname'])
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
            sql = "INSERT INTO `mechanics`(`Id_no`, `Firstname`, `Lastname`, `phoneno`, `location`, `areaofspecification`,`charge`, `email`, `password`, `photo`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor = conn.cursor()
            cursor.execute(sql, (idno, firstname, lastname, phoneno, location, areaofspecification, charge, email, password, encodedimage))
            conn.commit()
            return redirect('/')

            

    else:
        return render_template('register-m.html')






# run
if __name__ == '__main__':
    app.run(debug=True, port=5000)
# port = 10000