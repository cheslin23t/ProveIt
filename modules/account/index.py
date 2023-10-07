from flask import render_template, Blueprint, session, redirect, request
from ..database.index import mydb
import hashlib
import json
from datetime import datetime as Datetime
mycursor = mydb.cursor()
app = Blueprint('account', __name__, template_folder='../../templates')
def makeResponseJSON(success, message="Request processed successfully.", data={}):
    response = {
    "success": success,  # Indicates whether the operation was successful
    "message": message,  # A human-readable message
    "data": data
    }
    return response
def redirect_with_error(error_message, errorcode=302):
    return redirect("/error?message=" + error_message, errorcode)

@app.route('/login', methods=['POST'])
def loginRoute():
    try:
        if 'user' in session:
            return redirect('/')
        print(request.headers)
        username = request.form['username'].lower()
        passwordUnhashed = request.form['password']
        passwordHashed = hashlib.sha256(passwordUnhashed.encode('utf-8')).hexdigest()
        mycursor.execute("SELECT * FROM Users WHERE Username = %s AND Password = %s", (username, passwordHashed))

        if mycursor.fetchone():
            session['user'] = username
            return makeResponseJSON(True), 200
        else:
            return makeResponseJSON(False, "Incorrect username or password."), 401
    except Exception as e:
        print(e)
        return makeResponseJSON(False, str(e)), 500
@app.route('/signup', methods=["POST"])
def signupRoute():
    try:
        print('stage 1')
        print(request.form)
        if 'user' in session:
            return redirect('/')
        print('stage 2')
        if request.form.get('username'):
            print('stage 3')
            errorMsg = None
            # Defining Variables 
            username = request.form['username'].lower()
            print('stage 4')
            passwordUnhashed = request.form['password']
            print('stage 5')
            passwordHashed = hashlib.sha256(request.form['password'].encode('utf-8')).hexdigest()
            print('stage 6')
            firstName = request.form.get('firstName', None)
            print('stage 7')
            lastName = request.form.get('lastName', None)
            phoneNumber = request.form.get('phoneNumber', None)

           # Checks
            if len(passwordUnhashed) < 8:
                errorMsg = "Password is less than eight characters."
            if len(username) < 5:
                errorMsg = "Username is less than five characters."
            mycursor.execute("SELECT * FROM Users WHERE Username = %s", (username,))
            if mycursor.fetchone():
               errorMsg = "Account with this username already exists."
        
        
            if errorMsg:
                return makeResponseJSON(False, errorMsg), 400
        
            # Inserting into database

            mycursor.execute("INSERT INTO Users (Username, Password, FirstName, LastName, Phone, RegistrationDate) VALUES (%s, %s, %s, %s, %s, %s)", (username, passwordHashed, firstName, lastName, phoneNumber, Datetime.now()))
            mydb.commit()
            session['user'] = username
            return makeResponseJSON(True), 200
        else:
            return makeResponseJSON(False, "No username provided."), 400
    except Exception as e:
        print(e)
        return makeResponseJSON(False, str(e)), 500


@app.route('/account', methods=['GET'])
def accountRoute():
    if 'user' in session:
        return render_template('account.html', user=session.get('user'))
    else:
        return redirect('/#login?redirect=' + request.path)
@app.route('/logout')
def logoutRoute():
    del session['user']
    return redirect('/')