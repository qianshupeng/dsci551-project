import sys

if __name__ == "__main__":
    print("Welcome to ChatDB! \nAuthor: Qianshu Peng")
    while True:
        print("\nOptions: [1] Explore Dataset \n[2] Sample Queries \n[3] Upload Your Dataset \n[4] Exit")
        choice1 = input("Select an option: ")

        if choice1 == "1":
            print("\nChoose the Dataset: [1] sales")
            choice2 = input("Select a table: ")

        elif choice1 == "2":
            print("\nChoose a Built-in Dataset: [1] sales")

        elif choice1 == "3":
            file_path = input("Enter CSV file path: ")
            table_name = input("Enter name of the table: ")

        elif choice1 == "4":
            print("Goodbye! :)")
            sys.exit()
        
        else:
            print("Invalid Choice.")