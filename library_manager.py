import streamlit as st
import json

st.markdown("""
    <style>
        .stButton>button {
            background-color: #007BFF !important;
            color: white !important;
            border-radius: 5px;
            padding: 10px;
            width: 100% !important;
        }
        .stButton>button:hover {
            background-color: #0056b3 !important;
        }
    </style>
""", unsafe_allow_html=True)

class LibraryManager:
    def __init__(self, filename="library.json"):
        self.filename = filename
        self.library = self.load_library()

    def load_library(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_library(self):
        with open(self.filename, "w") as file:
            json.dump(self.library, file, indent=4)

    def add_book(self, title, author, year, genre, read_status):
        self.library.append({
            "title": title,
            "author": author,
            "year": int(year),
            "genre": genre,
            "read": read_status
        })
        self.save_library()

    def remove_book(self, title):
        self.library = [book for book in self.library if book["title"].lower() != title.lower()]
        self.save_library()

    def search_books(self, query):
        return [book for book in self.library if query.lower() in book["title"].lower() or query.lower() in book["author"].lower()]

    def display_statistics(self):
        total_books = len(self.library)
        read_books = sum(1 for book in self.library if book["read"])
        percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
        return total_books, percentage_read

manager = LibraryManager()

st.title("📚 Personal Library Manager")

menu = st.sidebar.radio("Menu", ["Add Book", "Remove Book", "Search Books", "Display All Books", "Statistics"])

if menu == "Add Book":
    st.header("Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=0, step=1)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Have you read this book?")
    if st.button("Add Book"):
        manager.add_book(title, author, year, genre, read_status)
        st.success("Book added successfully!")

elif menu == "Remove Book":
    st.header("Remove a Book")
    title = st.text_input("Enter the title of the book to remove")
    if st.button("Remove Book"):
        manager.remove_book(title)
        st.success("Book removed successfully!")

elif menu == "Search Books":
    st.header("Search for a Book")
    query = st.text_input("Enter title or author")
    if st.button("Search"):
        results = manager.search_books(query)
        if results:
            for book in results:
                st.markdown(f"### 📖 {book['title']}", unsafe_allow_html=True)
                st.markdown(f"- **Author:** {book['author']}\n- **Year:** {book['year']}\n- **Genre:** {book['genre']}\n- **Status:** {'✅ Read' if book['read'] else '❌ Unread'}")
        else:
            st.warning("No matching books found.")

elif menu == "Display All Books":
    st.header("Your Library")
    if not manager.library:
        st.warning("Your library is empty.")
    else:
        for book in manager.library:
            st.markdown(f"### 📖 <span style='color:blue;'>{book['title']}</span>", unsafe_allow_html=True)
            st.markdown(f"- **Author:** {book['author']}\n- **Year:** {book['year']}\n- **Genre:** {book['genre']}\n- **Status:** {'✅ Read' if book['read'] else '❌ Unread'}")

elif menu == "Statistics":
    st.header("Library Statistics")
    total_books, percentage_read = manager.display_statistics()
    st.write(f"**Total Books:** {total_books}")
    st.write(f"**Percentage Read:** {percentage_read:.2f}%")
