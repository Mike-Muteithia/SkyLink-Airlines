import json
import os

class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_borrowed = False

    def __str__(self):
        status = "Borrowed" if self.is_borrowed else "Available"
        return f"'{self.title}' by {self.author} (ISBN: {self.isbn}) - {status}"


class User:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.borrowed_books = []

    def __str__(self):
        return f"User: {self.name} (ID: {self.user_id})"


class Library:
    def __init__(self):
        self.books = []
        self.users = []
        self.data_file = "library_data.json"
        self.load_data()  # Attempt to load saved data when the library starts

    def load_data(self):
        """Reads the JSON file and reconstructs the objects."""
        if not os.path.exists(self.data_file):
            return  # If no file exists yet, start with an empty library
        
        with open(self.data_file, "r") as file:
            data = json.load(file)
            
        # Reconstruct Books
        for b in data.get("books", []):
            book = Book(b["title"], b["author"], b["isbn"])
            book.is_borrowed = b["is_borrowed"]
            self.books.append(book)
            
        # Reconstruct Users
        for u in data.get("users", []):
            user = User(u["name"], u["user_id"])
            # Link borrowed books back to the user
            for isbn in u["borrowed_books"]:
                book = self.find_book(isbn)
                if book:
                    user.borrowed_books.append(book)
            self.users.append(user)

    def save_data(self):
        """Converts objects to a dictionary and saves them to a JSON file."""
        data = {
            "books": [
                {"title": b.title, "author": b.author, "isbn": b.isbn, "is_borrowed": b.is_borrowed} 
                for b in self.books
            ],
            "users": [
                {"name": u.name, "user_id": u.user_id, "borrowed_books": [b.isbn for b in u.borrowed_books]} 
                for u in self.users
            ]
        }
        with open(self.data_file, "w") as file:
            json.dump(data, file, indent=4)

    def add_book(self, title, author, isbn):
        new_book = Book(title, author, isbn)
        self.books.append(new_book)
        print(f"Added book: '{title}'")
        self.save_data()  # Save after adding

    def register_user(self, name, user_id):
        new_user = User(name, user_id)
        self.users.append(new_user)
        print(f"Registered user: {name}")
        self.save_data()  # Save after registering

    def find_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def find_user(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    def borrow_book(self, user_id, isbn):
        user = self.find_user(user_id)
        book = self.find_book(isbn)

        if not user:
            print("Error: User not found.")
            return
        if not book:
            print("Error: Book not found.")
            return
        if book.is_borrowed:
            print("Sorry, that book is currently borrowed.")
            return

        book.is_borrowed = True
        user.borrowed_books.append(book)
        print(f"Success! {user.name} borrowed '{book.title}'.")
        self.save_data()  # Save after borrowing

    def return_book(self, user_id, isbn):
        user = self.find_user(user_id)
        book = self.find_book(isbn)

        if not user or not book:
            print("Error: User or Book not found.")
            return

        if book in user.borrowed_books:
            book.is_borrowed = False
            user.borrowed_books.remove(book)
            print(f"Success! '{book.title}' has been returned by {user.name}.")
            self.save_data()  # Save after returning
        else:
            print(f"Error: {user.name} does not have this book.")

    def display_books(self):
        if not self.books:
            print("The library has no books currently.")
            return
        print("\n--- Library Catalog ---")
        for book in self.books:
            print(book)
        print("-----------------------\n")


def main():
    library = Library()

    # Only add default demo data if the library is completely empty 
    # (meaning no save file exists yet)
    if not library.books and not library.users:
        library.add_book("1984", "George Orwell", "111")
        library.add_book("To Kill a Mockingbird", "Harper Lee", "222")
        library.register_user("Alice", "U1")

    while True:
        print("\n=== Library Management System ===")
        print("1. View all books")
        print("2. Add a new book")
        print("3. Register a new user")
        print("4. Borrow a book")
        print("5. Return a book")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            library.display_books()
        
        elif choice == '2':
            title = input("Enter book title: ")
            author = input("Enter author name: ")
            isbn = input("Enter ISBN: ")
            library.add_book(title, author, isbn)
        
        elif choice == '3':
            name = input("Enter user name: ")
            user_id = input("Enter user ID: ")
            library.register_user(name, user_id)
        
        elif choice == '4':
            user_id = input("Enter your User ID: ")
            isbn = input("Enter the Book ISBN to borrow: ")
            library.borrow_book(user_id, isbn)
        
        elif choice == '5':
            user_id = input("Enter your User ID: ")
            isbn = input("Enter the Book ISBN to return: ")
            library.return_book(user_id, isbn)
        
        elif choice == '6':
            print("Exiting the system. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()