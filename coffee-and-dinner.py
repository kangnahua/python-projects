"""
A script for recording group mates' delay to meetings
Rule for group meetings:
    1. If one is late for accumulated 15 minutes, he/she buys everyone coffee.
    2. If one is late 3 times, he/she invites everyone to dinner regardlessly of accumulative late time.
    3. Once punishment is fulfilled, one starts with clean slate again.
Running the script requires the following Python packages:
    sqlite3
The program runs in Python 3.
"""

import sqlite3
import time

def display():
    """Display execution choices and returns the corresponding execution for the user."""

    print('\n')
    print('-' * 50)
    print("{:^50}".format("Operation Table"))
    print('-' * 50)
    print("0. Initiate a new table for your team\n1. Update contents of your teammates' late time\n2. Show the current standing of your team's table\n3. Clearing current standing for punishments\n4. Deleting a table from the database\n5. List all tables in database\n6. Exit")
    
def list_tables():
    """Listing all available tables in coffee-and-dinner.db"""

    with sqlite3.connect("coffee-and-dinner.db") as connection:
        c = connection.cursor()
        c.execute("SELECT * from sqlite_master WHERE type='table';")
        tables = c.fetchall()

        print('*' * 50)
        if len(tables) == 0:
            print("The database is empty.")
        elif len(tables) != 0:
            i = 1
            print("Available tables in 'coffee-and-dinner.db':")
            for table in tables:
                print("%i. %s" % (i, table[1]))
                i += 1
        print('*' * 50)

def init_table():
    """Initiating a table in coffee-and-dinner.db if not existed."""

    team_name = input("Please type in the name of your team: ")
    create = input("Would you like to create a table (yes/no)? ").lower()
    if create.startswith('n'):
        print('No initiation of the table. Nothing is done.')
    elif create.startswith('y'):
        with sqlite3.connect("coffee-and-dinner.db") as connection:
            c = connection.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS {}(name TEXT, late_min INT, late_numbers INT);""".format(team_name))

            size = int(input("Please enter the number of teammates: "))
            for i in range(size):
                name = input("Enter name of teammate %i: " % (i+1))
                c.execute("INSERT INTO {} VALUES(?, ?, ?);".format(team_name), (name, 0, 0))
            connection.commit()


def delete_table():
    """Deleting a table in coffee-and-dinner.db if existed."""
    list_tables()

    prompt = "Please enter the name of table you want to delete: "
    table_name = input(prompt)
    print("Are you sure you want to delete table '{}'? (yes/no) ".format(table_name), end='')
    delete = input().lower()
    if delete.startswith('y'):
        with sqlite3.connect("coffee-and-dinner.db") as connection:
            c = connection.cursor()
            c.execute("DROP TABLE IF EXISTS {}".format(table_name))
            print("Table '{}' is now deleted.\n".format(table_name))
            connection.commit()
    elif delete.startswith('n'):
        print('Aborting deletion. Nothing is done.\n')

def update_content(team_name):
    """Updating data on a table inside coffee-and-dinner.db."""

    name = input("Please enter name of teammate who is late: ")

    with sqlite3.connect("coffee-and-dinner.db") as connection:
        c = connection.cursor()
        c.execute("SELECT late_min FROM {} WHERE name= ?".format(team_name), (name, ))
        cumulative_late_min = c.fetchone()[0]
        # note that  c.fetchone() returns a tuple (min, )
        cumulative_late_min += int(input("How many minutes is %s late: " % name))
        c.execute("SELECT late_numbers FROM {} WHERE name=?".format(team_name), (name, ))
        cumulative_late_numbers = c.fetchone()[0]
        cumulative_late_numbers += 1
        c.execute("UPDATE {} SET late_min = ? , late_numbers = ? WHERE name = ?;".format(team_name), (cumulative_late_min, cumulative_late_numbers, name))

        connection.commit()

def current_standing(team_name):
    """Displaying the current standing of late minutes and late numbers of each teammate."""

    with sqlite3.connect("coffee-and-dinner.db") as connection:
        c = connection.cursor()
        c.execute("SELECT * FROM {};".format(team_name))
        rows = c.fetchall()

        for r in rows:
            print("{0[0]:15s}\tlate minutes: {0[1]:2d}\tlate numbers: {0[2]:d}".format(r))

def clearing(team_name):
    """Printing out the punishments and clearing the standing for any teammate"""

    with sqlite3.connect("coffee-and-dinner.db") as connection:
        c = connection.cursor()

        # Printing punishment and clearing minutes for everyone
        c.execute("SELECT name FROM {} WHERE late_min >= 15".format(team_name))
        names_min = c.fetchall()

        print('\n' + '#' * 50)
        # name prints out ('name', ) as a tuple
        if len(names_min) != 0:
            for name in names_min:
                print("%s has exceeded 15 minutes and will buy everyone coffee." % name[0])
                c.execute("UPDATE {} SET late_min = 0 WHERE name= ? ;".format(team_name), (name[0], ))

        # Priting punishment and clearing late times for everyone
        c.execute("SELECT name FROM {} WHERE late_numbers >= 3".format(team_name))
        names_numbers = c.fetchall()
        # name prints out ('name', ) as a tuple
        if len(names_numbers) != 0:
            for name in names_numbers:
                print("%s has been late for 3 times and will invite everyone to dinner." % name[0])
                c.execute("UPDATE {} SET late_numbers = 0 WHERE name= ? ;".format(team_name), (name[0], ))

        if len(names_min) == 0 and len(names_numbers) == 0:
            print("Nobody has exceeded the limits for punishment yet.")
        print('#' * 50)
        connection.commit()
        time.sleep(1)
        print("\nCurrent standing after clearing is: ")
        current_standing(team_name)

if __name__ == "__main__":
    print('-' * 50)
    print("{:^50}\n".format("Welcome to Coffee-and-Dinner."))
    print('-' * 50 + '\n')
    time.sleep(1)

    with sqlite3.connect("coffee-and-dinner.db") as connection:
        c = connection.cursor()
        c.execute("SELECT * FROM sqlite_master WHERE type='table';")
        tables = c.fetchall()
        table_list = [table[1] for table in tables]


    switchboard = {'0':init_table, '1':update_content, '2':current_standing, '3':clearing, '4':delete_table, '5':list_tables}

    # Starting the program's user interface loop
    while True:
        display()
        time.sleep(1)
        argument = input("Please enter your choice of action: ")

        if argument == '6':
            break
        elif ord(argument) < ord('0') or ord(argument) > ord('6'):
            print("Please enter numbers between 0 and 5.")
            time.sleep(1)
        elif argument == '0' or argument == '4' or argument == '5':
            time.sleep(1)
            switchboard[argument]()
            time.sleep(1)
        else:
            team_name = input("Please enter the name of your team: ")
            if team_name not in table_list:
                print("Your team is not in the database yet.")
                print("Please choose option 0 to initiate a table.")
                time.sleep(1)
            else:
                time.sleep(1)
                switchboard[argument](team_name)
                time.sleep(1)
