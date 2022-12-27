from flask import *
import sqlite3

#____________________________________________________________________#
#                                                                    #
#       CISP 74 CRUD Web App Using Flask and Python Group Project    #
#               by Julian Arteaga and Yvette Vargas                  #
#                    Professor Sohair Zaki                           #
#                      November 27, 2022                             #
#                        application.py                              #
#____________________________________________________________________#

#____________________________________________________________________#
#                                                                    #
#                         Description:                               #
#  The main application for the web app using flask and python.      #
#  Contains each route and method for each page on the web app, and  #
#  how the web app connects to the database.                         #
#____________________________________________________________________#


app = Flask(__name__)

# index and login page
# takes out any active users just in case
@app.route("/")
def index():
    # establishes connection to database
    # truncates ActiveUsers in case of not properly logged out users
    with sqlite3.connect("movie_respo.db") as con:
        cur = con.cursor()
        cur.execute("DELETE FROM ActiveUsers")
        con.commit
    # returns which page to go to next and closes connection to database
    return render_template("index.html")
    con.close()

# index and login page if a username or password is wrong
@app.route("/index_wrong")
def index_wrong():
    return render_template("index_wrong.html")

# debug page to default to
@app.route("/other")
def other():
    return render_template("other.html")

# goes to if something wrong happened with user registration
@app.route("/wrong")
def wrong():
    return render_template("wrong.html")

# takes info from login page and checks if username and password are correct
# if correct then goes into site, if not then goes to index_wrong
@app.route('/theform', methods=['GET', 'POST'])
def theform():
    # sets up default page to fall back on
    nextPage = "other"
    # try block to get form data and interact with database
    try:
        # username and password from login page
        enteredUsername = request.form['userName']
        enteredPassword = request.form['password']
        # statement to be used for comparing entered username with username found in the User table
        statement = "SELECT * FROM Users WHERE username=\'" + enteredUsername + "\'"
        # connects to database and gets user's info
        con = sqlite3.connect("movie_respo.db")
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute(statement)
        user = cursor.fetchone()
        # compares username and password to see if correct
        # if correct, goes to requestMovie page
        if user["username"] == enteredUsername and user["password"] == enteredPassword:
            nextPage = 'requestMovie'
            try:
                # new connection to database to enter in the User into ActiveUsers table
                connnection = sqlite3.connect("movie_respo.db")
                cur = connnection.cursor()
                SQLstatement = "INSERT INTO ActiveUsers (username) VALUES (\'" + enteredUsername + "\')"
                cur.execute(SQLstatement)
                connnection.commit()
            # rolls back in case anything goes wrong
            except:
                connnection.rollback()
        # makes next page go to index_wrong if username or password is wrong
        else:
            nextPage = 'index_wrong'
    # goes to index_wrong as fallback if anything wrong happens
    except:
        nextPage = 'index_wrong'
    finally:
        # redirects to the next page and closes connections to the database
        return redirect(url_for(nextPage))
        con.close()
        connnection.close()

# requests for movies page which display movie table and request form
@app.route("/requestMovie")
def requestMovie():
    # takes Request table data to be sent to and displayed on the requestMovie page
    connection = sqlite3.connect("movie_respo.db")
    connection.row_factory = sqlite3.Row
    cur = connection.cursor()
    cur.execute("SELECT * from Requests")
    rows = cur.fetchall()
    return render_template('requestMovie.html', rows=rows)
    connection.close()

# saves movie request data and puts it into Requests table, goes back to requestMovie page
@app.route("/saverequest",methods = ["POST","GET"])
def saveRequest():
    # makes connection to database and retrives user in ActiveUsers for data in Requests table
    msg = "msg"
    con = sqlite3.connect("movie_respo.db")
    cur = con.cursor()
    con.row_factory = sqlite3.Row
    cur.execute("SELECT * FROM ActiveUsers")
    user = cur.fetchall()
    # variable for username fetched from ActiveUsers
    name = user[0][1]
    # takes info from form and puts it into Requests table
    if request.method == "POST":
        # takes info from form on requestMovie and inputs it into Requests
        try:
            title = request.form["title"]
            year = request.form["Year"]
            genre = request.form["genre"]
            director = request.form["director"]
            subtitle = request.form["subtitle"]
            purpose = request.form["purpose"]
            status = "In Review"
            with sqlite3.connect("movie_respo.db") as connection:
                cursor = connection.cursor()
                cursor.execute("INSERT into Requests (title, year, genre, director, subtitle, purpose, status, username) values (?,?,?,?,?,?,?,?)",(title, year, genre, director, subtitle, purpose, status, name))
                connection.commit()
                msg = "Request successfully Submitted"
        # rolls back if anything goes wrong and doesn't add to Requests table
        except:
            connection.rollback()
            msg = "We can not add that request to the database"
        finally:
            return redirect(url_for("requestMovie", msg = msg))
            connection.close()

# user registration page that contains the user_reg form
@app.route("/user_reg")  
def user_reg():  
    return render_template("user_reg.html");  
 
# user registration page that saves all info into Users table
@app.route("/user_sub",methods = ["POST","GET"])  
def user_sub():  
    # fallbacks for message and nextPage
    msg = "some error happened" 
    nextPage = "other" 
    if request.method == "POST":  
        # takes form data from user_reg page and makes sure they are strings
        # inputs them into the User table and goes back to index to login
        try:  
            first = str(request.form["first"])  
            middle = str(request.form["middle"])
            last = str(request.form["last"])
            DateOfBirth = request.form["DOB"]
            email = str(request.form["email"])  
            gender = str(request.form["gender"])
            username = str(request.form["username"])
            password = str(request.form["password"])
            disability = str(request.form["disability"])
            with sqlite3.connect("movie_respo.db") as con:  
                cur = con.cursor()  
                cur.execute("INSERT into Users (first, middle, last, DOB, email, gender, username, password, disability) values (?,?,?,?,?,?,?,?,?)",(first, middle, last, DateOfBirth, email, gender, username, password, disability))  
                con.commit()  
                msg = "User successfully Added"  
                nextPage = "index"
        # goes to wrong page in case username or email is already taken
        except:  
            nextPage = "wrong"
            con.rollback()  
            msg = "We can not add the user to the list"
        finally:  
            return redirect(url_for(nextPage, msg=msg))
            con.close()  
            
# gets and shows user info as well as past requests in a table
@app.route("/profile")
def profile():
    connection = sqlite3.connect("movie_respo.db")
    connection.row_factory = sqlite3.Row
    cur = connection.cursor()
    cur.execute("SELECT * from ActiveUsers")
    user = cur.fetchall()
    # fetches user info from Users table based on username in ActiveUsers
    with sqlite3.connect("movie_respo.db") as con:
        statement = "SELECT * FROM Users WHERE username =\'" + user[0]["username"] + "\'"
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute(statement)
        account = cursor.fetchone()
    # fetches Requests data only made by user
    with sqlite3.connect("movie_respo.db") as conn:
        SQLstatement = "SELECT * FROM Requests WHERE username =\'" + user[0]["username"] + "\'"
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()
        curs.execute(SQLstatement)
        rows = curs.fetchall()
    
    return render_template("profile.html", account=account, rows=rows)
    connection.close()
    con.close()
    conn.close()

# shows editable user info to be updated
@app.route("/update")
def update():
    # gets username from ActiveUsers
    with sqlite3.connect("movie_respo.db") as connection:
        connection.row_factory = sqlite3.Row
        cur = connection.cursor()
        cur.execute("SELECT * from ActiveUsers")
        user = cur.fetchone()
    # gets user info from User table
    with sqlite3.connect("movie_respo.db") as con:
        statement = "SELECT * FROM Users WHERE username =\'" + user["username"] + "\'"
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute(statement)
        account = cursor.fetchone()

    return render_template("update.html", account=account)
    connection.close()
    con.close()

# takes edited user info and saves it
@app.route("/updateUser", methods = ["POST", "GET"])
def updateUser():
    msg='msg'
    with sqlite3.connect("movie_respo.db") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * from ActiveUsers")
        user = cursor.fetchone()

    if request.method == "POST":  
        # takes user info to be updated in the User table
        try:  
            first = request.form["first"]  
            middle = request.form["middle"]
            last = request.form["last"]
            DateOfBirth = request.form["DOB"]
            email = request.form["email"]  
            gender = request.form["gender"]
            username = request.form["username"]
            password = request.form["password"]
            disability = request.form["disability"] 
            with sqlite3.connect("movie_respo.db") as con:  
                cur = con.cursor()  
                cur.execute("UPDATE Users SET first=?, middle=?, last=?, DOB=?, email=?, gender=?, username=?, password=?, disability=? WHERE username =?",(first, middle, last, DateOfBirth, email, gender, username, password, disability, user["username"]))  
                con.commit()  
                msg = "User successfully updated" 
        # rolls back just in case anything happens 
        except:  
            con.rollback()  
            msg = "We can not update the user"  
        finally:  
            return redirect(url_for("profile", msg=msg))
            connection.close()
            con.close()

# takes User to delete page to ask for confirmation before deleting
@app.route("/delete")  
def delete():  
    return render_template("delete.html")  
 
# delete User page for deleting User info from database
@app.route("/deleteUser")  
def deleterecord():  
    msg='msg'
    # gets username from ActiveUsers to delete the user from the User table
    with sqlite3.connect("movie_respo.db") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * from ActiveUsers")
        user = cursor.fetchone()
    Statement = "DELETE from Users WHERE username=\'" + user['username'] + "\'"
    with sqlite3.connect("movie_respo.db") as con:  
        # tries to delete the user and then takes them to delete_record page
        try:  
            cur = con.cursor()  
            cur.execute(Statement)  
            msg = "record successfully deleted"  
        except:  
            msg = "can't be deleted"  
        finally:  
            return render_template("delete_record.html", msg = msg)  
            connection.close()
            con.close()

# logs user off by deleting them from the ActiveUsers table and takes them back to index
@app.route("/logoff")
def logoff():
    # truncates ActiveUsers tables
    with sqlite3.connect("movie_respo.db") as con:
        cur = con.cursor()
        cur.execute("DELETE FROM ActiveUsers")
        con.commit
        return redirect(url_for("index"))
        con.close()




# runs the main program
if __name__ == "__main__":
    app.run(debug = True)  