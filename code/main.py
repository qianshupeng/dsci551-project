# main.py
# interface and main running logic of ChatDB

import sys
import os


if __name__ == "__main__":
    print("Welcome to ChatDB! \nBy Qianshu Peng")

    print("Initialization...")
    while True:
        print("\nOptions: \n[1] Explore Database \n[2] Sample Queries \n[3] Upload Your Database \n[4] Exit")
        print("At any time, type \"Back\" to go back and \"Menu\" to go to the main menu.")
        choice1 = input("Select an option: ")

        if choice1 == "1":
            print("\nChoose a Built-in Database: [1] sales")
            choice2 = input("Select a table: ")

        elif choice1 == "2":
            print("\nChoose a Built-in Database: [1] sales")

        elif choice1 == "3":
            file_path = input("Enter CSV file path: ")
            table_name = input("Enter name of the table: ")

        elif choice1 == "4":
            print("Goodbye! :)")
            sys.exit()
        
        else:
            print("Invalid Input")