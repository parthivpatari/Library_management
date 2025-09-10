def Library_Managment():
    Books = []

    while True:
        print("\n1. Buy Book"
              "\n2. Sell Book"
              "\n3. Find Book"
              "\n4. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            book = input("Enter Book Name to Buy: ").lower()
            Books.append(book)
            print(f"Book '{book}' added to library.")

        elif choice == "2":
            book = input("Enter Book Name to Remove: ").lower()
            if book in Books:
                Books.remove(book)
                print(f"Book '{book}' removed from library.")
            else:
                print("No Book Found.")

        elif choice == "3":
            if not Books:
                print("No books in library.")
            else:
                print("Books in library:")
                for book in Books:
                    print("- " + book)

        elif choice == "4":
            print("Exiting Library Management System...")
            break

        else:
            print("Invalid choice! Try again.")

Library_Managment()


