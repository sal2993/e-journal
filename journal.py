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
#

import sys
from datetime import date, datetime
import getpass
import Model
import hashlib
import uuid

def main():

    user_rows = get_usernames_fDB()

    # Log into or create user, Always returns User's ID key
    user_primary_key = log_in(user_rows)

    # Introduce program
    user_option = menu_options()

    # User wants to enter a new journal entry
    if user_option == 1:
        # Open a text editor or accept input from command line
        users_input = user_entry_input()
        # Enter user input to DB
        to_database(users_input, user_primary_key)

    # User wants to enter a new task
    elif user_option == 2:
        # Open User To-Do List
        users_input = input_task_todo()
    
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

        # Check whether new user
        # IF new user, create user and return new user object
        if login_attempt == '-1':
            new_user = create_user()
            x = False
            return new_user

        # Check for existing user, check credentials
        else:
            # check if the username is in db
            if user_exists(login_attempt):

                # Get the user object
                user = get_user(login_attempt)

                # Ask for password
                passw = getpass.getpass(u"Password: ")
                
                if check_password(passw, user.password) :
                    x = False
                    return user # return user's primary key is needed
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
        print "2 - View your 'To-Do's"
        print "1 - Make an Entry"
        print "0 - Exit"
        x = raw_input("> ")

        if x == '0':
            sys.exit(0)
        elif x == '1':
            return 1
            looper = False
        elif x == '2':
            return 2
            looper = False
            
    return 0

# ***************************************************************************** 
# This will be where we get the users input    
#
# Note: I have an idea that I want the user to be able to enter journal
# entries from the command line or from their chosen text editor. In order to
# to be able to enter from the command line, they should be able to type:
#   journal -m "Their own stuff that they want to add into their entries"
# otherwise it will open their default text editors.
#
def user_entry_input():

    print '\n' + str(date.today()) + ':'
    user_entry = raw_input(">> ")
    return user_entry

# Add a salt and hash users password before saving to the database
# @: takes user's password
# $: returns users hashed password and salt
def encode(password):
    # generate salt
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + \
        ':' + salt

# Check if the user input password matches the hashed password + salt in db
def check_password(input_password, encoded_password):
    hashed_password, salt = encoded_password.split(':')
    if hashlib.sha256(salt + input_password).hexdigest() == hashed_password :
        return True
    else:
        return False

def input_task_todo():
    return

# ************************ DATABASE - FUNCTIONS ******************************* 
# ********************************* - ***************************************** 

# Check if the username is in the user table
def user_exists(user):
    query = Model.User.select().where(Model.User.username == user)
    if query.exists():
        return True
    else:
        return False

# return user object from Database
# Error is the username does not exist
def get_user(username):
    try:
        user = Model.User.get(Model.User.username == username)
        return user
    except Exception as e:
        print "failed to find user %s! Error 2"%username
        sys.exit(2)



def checktables():
    # cur.execute("CREATE TABLE IF NOT EXISTS Temporary(Id INT)
    return

# Creates a User. Also returns the new users ID to properly add post to DB.
def create_user():

    
    uname = raw_input("[new] Username: ")       # Get username
    
    new_password = getpass.getpass('Password: ')    # Get password

    hashed_password = encode(new_password)
    
    # insert user info into user table in Model
    user = Model.User(username=uname, password=hashed_password)
    user.save()
            
    # return new user's ID
    return user

# ***************************************************************************** 
def to_database(users_input, user_primary_key):

    # keep dates as gregorian ordinal
    todays_date = date.today()

    # Enter data to database *that was easy*
    Model.Entry.create(owner_id=user_primary_key, body=users_input, \
        timestamp=todays_date)
    return

        
if __name__ == '__main__':
    main()
