'''
0157Al211007
Aditya Choudhary
CSE-AIML LNCTS
'''

import mysql.connector as c
import random
from mysql.connector import IntegrityError


def create_connection():
    connection = c.connect(host="localhost", user="root", password="1234", database="school")
    return connection

def register(cursor):
    username = input("Enter the username: ")
    password = input("Enter the password: ")

    query = "INSERT INTO student (username , password) VALUES (%s, %s)"
    # cursor.execute(query, (username , password))
    # print("User registered successfully.")
    try:
        cursor.execute(query, (username , password))
        print("User registered successfully.")
    except IntegrityError as ie:
        print("Username exists, try different username")


def login(cursor, connection):
    username = input("Enter username: ")
    password = input("Enter password: ")

    query = "SELECT * FROM student WHERE username = %s AND password = %s"
    cursor.execute(query, (username , password))
    user = cursor.fetchone()

    if user is not None and user[0] == username and user[1] == password:
        print("Login successful!!!\n")
        services(cursor,username,connection)
    else:
        print("Invalid credentials. Please try again.")

    return username

def services(cursor, username, connection):
    print("1. See Profile")
    print("2. Attempt Quiz")
    print("3. See Result")
    print("4. Logout")
    
    choice = input("Enter your choice: ")
    if(choice=='1'):
        profile(cursor, username)
    elif(choice=='2'):
        attempt_quiz(cursor, username, connection)
    elif(choice=='3'):
        result(cursor, username)
    elif (choice=='4'):
        print("Logged out successfully !!!")
        exit()
    else:
        print("Invalid Choice!!! Try again\n")
    services(cursor, username, connection)
def profile(cursor, username):
    print("Your Profile :- ")
    print("Username - " + username)
    cursor.execute("Select high_score from student where username =  %s", (username,))
    high_score_row = cursor.fetchone()
    high_score = high_score_row[0]
    print("Your Highest Score - " + str(high_score)+"\n")

def result(cursor, username):
    cursor.execute("Select high_score from student where username =  %s", (username,))
    high_score_row = cursor.fetchone()
    high_score = high_score_row[0]
    print("Your Highest Score - " + str(high_score)+"\n")

def attempt_quiz(cursor, username, connection):
    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()
    random.shuffle(questions)
    cnt = 1
    curr_score = 0

    # Iterate through the questions and quiz the user
    for qno, quest, ans, option1, option2, option3, option4 in questions:
        print(f"\nQuestion {cnt}: {quest}")
        print("Options:")
        que_list = {1: option1, 2: option2, 3: option3, 4: option4}
        print(f"1. {que_list[1]}")
        print(f"2. {que_list[2]}")
        print(f"3. {que_list[3]}")
        print(f"4. {que_list[4]}")

        user_answer = int(input("Your answer (enter the option number): "))
        if user_answer > 4 or user_answer < 1:
            print("\nInvalid choice!\n")
        elif que_list[user_answer] == ans:
            print("Correct!\n")
            curr_score += 1
        else:
            print(f"Wrong! The correct answer is {ans}\n")
        cnt += 1

    print(f"You have scored {curr_score} points by giving {curr_score} right answers\n")

    cursor.execute("SELECT high_score FROM student WHERE username = %s", (username,))
    high_score_row = cursor.fetchone()
    high_score = high_score_row[0]

    if curr_score > high_score:
        cursor.execute("UPDATE student SET high_score = %s WHERE username = %s", (curr_score, username))
        connection.commit()
        

    
def main():
    connection = create_connection()
    cursor = connection.cursor()

    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            register(cursor)
        elif choice == '2':
            username = login(cursor, connection)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")
        connection.commit()

    connection.close()
    attempt_quiz(cursor)

main()
