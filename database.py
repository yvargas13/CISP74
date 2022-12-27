import sqlite3

#____________________________________________________________________#
#                                                                    #
#       CISP 74 CRUD Web App Using Flask and Python Group Project    #
#               by Julian Arteaga and Yvette Vargas                  #
#                    Professor Sohair Zaki                           #
#                      November 27, 2022                             #
#                         database.py                                #
#____________________________________________________________________#

#____________________________________________________________________#
#                                                                    #
#                         Description:                               #
#  The python file to define and start the database to use for the   #
#  web app. Autopopulates two of the databases with sample data put  #
#  in them.                                                          #
#____________________________________________________________________#

# create connection to database
connection = sqlite3.connect("movie_respo.db")
print("Database opened successfully")
# create cursor for inputting statements
cursor = connection.cursor()

# drop statements for refreshing tables
# cursor.execute("drop table Requests")
# cursor.execute("drop table Users")
# cursor.execute("drop table ActiveUsers")


# creates Requests table to keep track of all movie requests and who made the said request
connection.execute("""create table Requests (id INTEGER PRIMARY KEY AUTOINCREMENT, 
    title TEXT NOT NULL, 
    year YEAR NOT NULL, 
    genre TEXT NOT NULL, 
    director TEXT NOT NULL, 
    subtitle TEXT NOT NULL, 
    purpose TEXT,
    status TEXT NOT NULL,
    username TEXT NOT NULL)""")

print("Table created successfully")

# populates Requests table with sample data
connection.execute("""INSERT into Requests (title, year, genre, director, subtitle, purpose, status, username) values 
    ("Big Fish", 2003, "Fantasy", "Tim Burton", "YES", "School project", "Completed", "JArt1027")""")

connection.execute("""INSERT into Requests (title, year, genre, director, subtitle, purpose, status, username) values 
    ('Life of Pi', 2012, 'Fantasy', 'Ang Lee', 'NO', 'For my little girl', 'Completed', 'Persona5')""")

connection.execute("""INSERT into Requests (title, year, genre, director, subtitle, purpose, status, username) values 
    ('Goodfellas', 1990, 'Drama', 'Martin Scorsese', 'YES', 'Movie club at school', 'Completed', 'YvetteVY')""")

connection.execute("""INSERT into Requests (title, year, genre, director, subtitle, purpose, status, username) values 
    ('The Usual Suspects', 1995, 'Mystery', 'Bryan Singer', 'YES', 'Another for movie club', 'Completed', 'YvetteVY')""")

connection.execute("""INSERT into Requests (title, year, genre, director, subtitle, purpose, status, username) values 
    ('Sliver Lining Playbook', 2012, 'Romance', 'David O. Russell', 'NO', 'Another school project', 'Pending', 'JArt1027')""")

connection.execute("""INSERT into Requests (title, year, genre, director, subtitle, purpose, status, username) values 
    ("One Flew Over the Cuckoo's Nest", 1975, "Drama", "Milos Forman", "NO", "For my friend", "Pending", "Persona5")""")

connection.execute("""INSERT into Requests (title, year, genre, director, subtitle, purpose, status, username) values 
    ("The Great Gatsby", 2013, "Romance", "Baz Luhrmann", "YES", "School project", "In Review", "AASmith")""")

connection.execute("""INSERT into Requests (title, year, genre, director, subtitle, purpose, status, username) values 
    ("The Grand Budapest Hotel", 2014, "Comedy", "Wes Anderson", "YES", "school movie club", "In Review", "YvetteVY")""")

connection.commit()


# creates Users table to keep track of all users registered with website
connection.execute("""create table Users 
(id INTEGER PRIMARY KEY AUTOINCREMENT, 
first TEXT NOT NULL, 
middle TEXT NOT NULL, 
last TEXT NOT NULL, 
DOB DATE NOT NULL, 
email TEXT UNIQUE NOT NULL, 
gender TEXT NOT NULL, 
username TEXT UNIQUE NOT NULL, 
password TEXT NOT NULL, 
disability TEXT NOT NULL )""")  
  
print("Table created successfully") 

# populates Users table with sample users
connection.execute("""INSERT INTO Users (first, middle, last, DOB, email, gender, username, password, disability) values
    ("Julian", "Aaron", "Arteaga", "10/27/1994", "julian.arteaga16@gmail.com", "Male", "JArt1027", "Password1", "Learning Disability")""")

connection.execute("""INSERT INTO Users (first, middle, last, DOB, email, gender, username, password, disability) values
    ("Person", "Human", "Dude", "01/15/2001", "personDude@gmail.com", "Male", "Persona5", "DudeComes2", "")""")

connection.execute("""INSERT INTO Users (first, middle, last, DOB, email, gender, username, password, disability) values
    ("Aaron", "", "Smith", "08/20/1997", "aasmith10@gmail.com", "Transgender", "AAsmith", "Smithers3", "Helper for disabled")""")

connection.execute("""INSERT INTO Users (first, middle, last, DOB, email, gender, username, password, disability) values
    ("Yvette", "", "Vargas", "06/05/1998", "yvettevy@gmail.com", "Female", "YvetteVY", "Vetties4", "")""")

connection.commit()


# creates ActiveUsers table to keep track of which user is currently on the website using it
# meant to only have one user at a time and be empty the rest of the time
connection.execute("""create table ActiveUsers (id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL)""")

print("Table created successfully")

# closes connection to database
connection.close()