#!/usr/bin/env python

# This program is a hacker's journal entries.
# This program had 1 main function 'Keep a database of peoples entries'
# Other Functions:
#   View Entries, Delete Entries, Search entries.

# Additional features that i would like to have: Encrypted entries,
#   User accounts, Set up SHH Key logins, and a BareBones web app.

# Why am I doing this? Penzu sucks, i mean it reeeaaally sucks. its too fancy.
# Keep Open Source and Free as long as possible.

import sys
import sqlite3 as lite
from datetime import date, datetime

def main():

    # Introduce program
    welcome_menu()

    # Open a text editor or just accept user input from the command line
    users_entry = user_input()

    # Enter user input to DB
    to_database(users_entry)

#   con = lite.connect('test.db')
#   with con:
#       cur = con.cursor()
#       cur.execute("SELECT * FROM Test")
#       rows = cur.fetchall()
#       for row in rows:
#           print row
    print "worked."
    return 0

# ***************************************************************************** 
# Simple Welcome Menu with options to enter entry and exit
def welcome_menu():
    # Print many new lines
    for i in range(50):
        print "\n"

    print "Greetings, welcome to QEntries"
    print "  A -Sal Camara- Program  "

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
def user_input():

    print '\n' + str(date.today()) + ':'
    user_entry = raw_input(">> ")
    print user_entry
    return user_entry

def to_database(users_input):

    ordinal_date = date.toordinal(date.today())
    
    # need to change into to tuple to insert into the database with cur.execute
    info_for_db = (ordinal_date, users_input)
    
    # connect to database
    con = lite.connect('test.db')
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO Test VALUES(?,?)", info_for_db)
    print 'users input succesfully put into db'
    return

        
if __name__ == '__main__':
    main()
