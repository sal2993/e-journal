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

    # Log into or create user, Always returns User's ID key
    user_primary_key = log_in(user_rows)

    # Introduce program
    menu_options()

    # Open a text editor or accept input from command line
    users_entry = user_input()

    # Enter user input to DB
    to_database(users_entry, user_primary_key)

    print "Recorded. "
    return 0

# ***************************************************************************** 
# A login/sign-up function. also a quick greeting.
def log_in(users):

    # Print many new lines
    print "\nGreetings, welcome to QEntries"

    x = True
    while(x):
        
        print '||New user? Type -1||'
        login_attempt = raw_input(u"Username: ")

        if login_attempt == '-1':       # Check whether new user
            new_user_id = create_user()
            x = False
            return new_user_id

        else:                           # Existing user, Check credentials
            for user in users:
                # check if the username is in db
                if user[1] == login_attempt:
                
                    # if user is in db, check their password.
                    passw = getpass.getpass(u"Password: ")
                    
                    if passw == user[2]:
                        x = False
                        return user[0] # return user's primary key is needed
                    print 'your user name was found!'
                    # ask for password #
    sys.exit(2)
    return


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
# Creates a User. Also returns the new users ID to properly add post to DB.
def create_user():

    
    uname = raw_input("[new] Username: ")       # Get username
    
    password = getpass.getpass('Password: ')    # Get password
    
    user_creds = (uname, password)              # Add to Tuple

    # Enter new information to DB
    con = lite.connect('entries.db')
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO Users(username, password) VALUES(?, ?)" \
        , user_creds)
        
        # Grab the new users ID
        last_id = cur.lastrowid 
    return last_id

# ***************************************************************************** 
def get_usernames_fDB():
    con = lite.connect('entries.db')
    with con:
        cur = con.cursor()
        cur.execute("Select * FROM Users")
        rows = cur.fetchall()
    return rows

# ***************************************************************************** 
def to_database(users_input, user_primary_key):

    # keep dates as gregorian ordinal
    ordinal_date = date.toordinal(date.today())
    
    # Entry into to tuple (needed to enter db)
    info_for_db = (ordinal_date, users_input, user_primary_key)
    
    # connect to database
    con = lite.connect('entries.db')
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO Entries(Body, Date, UserId) VALUES(?,?, ?)" \
        , info_for_db)
    return

        
if __name__ == '__main__':
    main()
