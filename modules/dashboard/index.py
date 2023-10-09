from flask import render_template, Blueprint, session, redirect, request
from ..utils.database import mydb
from ..utils.error import makeResponseJSON

mycursor = mydb.cursor(dictionary=True)
app = Blueprint('dashboard', __name__, template_folder='../../templates')



@app.route('/dashboard', methods=['GET'])
def accountRoute():
    if 'user' in session:
        mycursor.execute("SELECT * FROM Users WHERE Username = %s", (session['user'],))
        result = mycursor.fetchone()
        if result:
            print(result)
            return render_template('dashboard.html', user=result)
        else:
            return makeResponseJSON(False, "Session and database username mismatch.", 500)
    else:
        return redirect('/?promptLogin=1&redirect=' + request.path)