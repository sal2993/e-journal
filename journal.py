#!/usr/bin/env python

# This program is a hacker's journal entries.
# This program had 1 main function 'Keep a database of peoples entries'
# Other Functions:
#   LOG IN, View Entries, Delete Entries, Search entries.

# Additional features that i would like to have: Encrypted entries,
#   User accounts, Set up SHH Key logins, and a BareBones web app.

# Why am I doing this? Penzu sucks, i mean it reeeaaally sucks. its too fancy.
# Keep Open Source and Free as long as possible.
#
# UPDATE (Sept 26, 2016): I will make a quick local journal program then
#   Proceed to make a web server version, maybe with SSH storage abilities...

import sys
import sqlite3 as lite
from datetime import date, datetime
import getpass

def main():

    user_rows = get_usernames_fDB()

    # Log into or create user
    log_in(user_rows)

    # Introduce program
    menu_options()

    # Open a text editor or accept input from command line
    users_entry = user_input()

    # Enter user input to DB
    to_database(users_entry)

#   con = lite.connect('entries.db')
#   with con:
#       cur = con.cursor()
#       cur.execute("SELECT * FROM Test")
#       rows = cur.fetchall()
#       for row in rows:
#           print row
    print "worked."
    return 0

# ***************************************************************************** 
# A login/sign-up function. also a quick greeting.
def log_in(users):

    # Print many new lines
    for i in range(50):
        print "\n"

    print "Greetings, welcome to QEntries"
    print "  A -Sal Camara- Program  \n\n"

    x = True
    while(x):
        
        print '"If you are a new user type -1 into user"\n'
        login_attempt = raw_input(u"Username: ")

        # Check whether new user, otherwise check against current users
        if login_attempt == '-1':
            create_user()
            x = False
        else:
            for user in users:
                print user
                user_string = user[0]   # Take String from Tuple

                # check if the username is in db
                if user[0] == login_attempt:
                    passw = getpass.getpass(u"Password: ")
                    # if user is in db, check their password.
                    if passw == user[1]:
                        x = False
                    print 'your user name was found!'
                    # ask for password #


# ***************************************************************************** 
# Simple Welcome Menu with options to enter entry and exit
def menu_options():


    looper = True
    while(looper):
        print "Please enter a number."
        print "1 - Make an Entry"
        print "0 - Exit"
        x = raw_input("> ")
        if x == '1':
            looper = False
        elif x == '0':
            sys.exit(0)
    return

# ***************************************************************************** 
# This will be where we get the users input    
#
# Note: I have an idea that I want the user to be able to enter journal
# entries from the command line or from their chosen text editor. In order to
# to be able to enter from the command line, they should be able to type:
#   journal -m "Their own stuff that they want to add into their entries"
# otherwise it will open their default text editors.
#
def user_input():

    print '\n' + str(date.today()) + ':'
    user_entry = raw_input(">> ")
    print user_entry
    return user_entry

# ************************ DATABASE - FUNCTIONS ******************************* 
# ********************************* - ***************************************** 
def create_user():
    
    uname = raw_input("[new] Username: ")
    password = getpass.getpass('Password: ')
    user_creds = (uname, password)

    con = lite.connect('entries.db')
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO User VALUES(?, ?)", user_creds)
    return

# ***************************************************************************** 
def get_usernames_fDB():
    con = lite.connect('entries.db')
    with con:
        cur = con.cursor()
        cur.execute("Select name, password FROM User")
        rows = cur.fetchall()
    return rows

# ***************************************************************************** 
def to_database(users_input):

    ordinal_date = date.toordinal(date.today())
    
    # need to change into to tuple to insert into the database with cur.execute
    info_for_db = (ordinal_date, users_input)
    
    # connect to database
    con = lite.connect('entries.db')
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO Entries VALUES(?,?)", info_for_db)
    print 'users input succesfully put into db'
    return

        
if __name__ == '__main__':
    main()
