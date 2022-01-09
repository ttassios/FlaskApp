from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'ergasiathemis'

def connect_with_database():
    return sqlite3.connect('DBergasias.db')


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/loginpage')
def loginpage():
    return render_template('loginpage.html')

@app.route('/registerpage')
def registerpage():
    return render_template('register.html')



@app.route('/register.html', methods=['POST', 'GET'])
def register():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('DBergasias.db')
        cur = conn.cursor()
        checkIfusernameExists = "SELECT * FROM users WHERE username = ?"
        cur.execute(checkIfusernameExists, [username])
        user = cur.fetchone()
        if user:
            message = 'Υπάρχει ήδη χρήστης με αυτό το όνομα!'
        elif not username or not password:
            message = 'Δεν συμπληρώσατε σωστά την φόρμα!'
        else:
            cur.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, password))
            conn.commit()
            message = 'Ο νέος χρήστης δημιουργήθηκε με επιτυχία'
    return render_template('register.html', message=message)

@app.route('/loggedin.html', methods=['POST', 'GET'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('DBergasias.db')
        cur = conn.cursor()
        checkIfUserExists = "SELECT * FROM users WHERE username = ? AND password = ?"
        cur.execute(checkIfUserExists, [username, password])
        user = cur.fetchone()
        if user:
            session['loggedin'] = True
            session['id'] = user[0]
            session['username'] = user[1]
            return render_template('loggedin.html')
        else:
            invalid = 'Δοκιμάστε ξανά!'
            return render_template('loginpage.html', invalid=invalid)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/loggedin')
def loggedin():
    if 'loggedin' in session:
        return render_template('loggedin.html')
    else:
        return render_template('index.html')

@app.route('/addguest', methods=['POST', 'GET'])
def addguest():
    if 'loggedin' in session:
        firstname = request.form['firstname']
        surname = request.form['surname']
        phonenumber = request.form['phonenumber']
        date = request.form['date']
        time = request.form['time']
        conn = sqlite3.connect('DBergasias.db')
        cur = conn.cursor()
        insertGuest = 'INSERT INTO guests (firstname, surname, phonenumber, date, time) VALUES (?,?,?,?,?)'
        cur.execute(insertGuest, [firstname, surname, phonenumber, date, time])
        conn.commit()
        mesg = 'Το ραντεβού δημιουργήθηκε επιτυχώς'
        return render_template('loggedin.html', mesg=mesg)
    else:
        return render_template('index.html')

@app.route('/guests')
def guests():
    conn = sqlite3.connect('DBergasias.db')
    cur = conn.cursor()
    sel = cur.execute("SELECT guest_id, firstname, surname, phonenumber, date, time FROM guests")
    additions = []
    for row in sel.fetchall():
        additions.append(dict(guest_id=row[0], firstname=row[1], surname=row[2], phonenumber=row[3], date=row[4], time=row[5]))
    print(additions)
    return render_template('guests.html', additions=additions)


@app.route('/guests/<int:guest_id>', methods=['POST', 'GET'])
def editguest(guest_id):
    if 'loggedin' in session:
        conn = sqlite3.connect('DBergasias.db')
        cur = conn.cursor()
        sel = cur.execute("SELECT guest_id, firstname, surname, phonenumber, date, time FROM guests WHERE guest_id=?", [guest_id])
        rv = sel.fetchall()
        print(rv)
        guest = rv[0]
        print(guest)
        return render_template('update.html', guest=guest)
    else:
        return redirect(url_for('index'))

@app.route('/updateguest', methods=['POST', 'GET'])
def updateguest():
    if request.method == 'POST':
        guest_id = request.form['guest_id']
        firstname = request.form['firstname']
        surname = request.form['surname']
        phonenumber = request.form['phonenumber']
        date = request.form['date']
        time = request.form['time']
        conn = sqlite3.connect('DBergasias.db')
        cur = conn.cursor()
        update_sql = "UPDATE guests SET firstname=?, surname=?, phonenumber=?, date=?, time=? WHERE guest_id=?"
        cur.execute(update_sql, [firstname, surname, phonenumber, date, time, guest_id])
        conn.commit()
        return redirect(url_for('guests'))

@app.route('/deleteguest/<int:guest_id>', methods=['POST', 'GET'])
def deleteguest(guest_id):
    if 'loggedin' in session:
        conn = sqlite3.connect('DBergasias.db')
        cur = conn.cursor()
        delete_sql = "DELETE FROM guests WHERE guest_id=?"
        cur.execute(delete_sql, [guest_id])
        conn.commit()
        return redirect(url_for('guests'))
    else:
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)