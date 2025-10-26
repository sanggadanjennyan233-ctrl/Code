import tkinter as tk
from tkinter import messagebox, ttk


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def add_book(self, book):
        new_node = Node(book)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def get_all_books(self):
        books = []
        current = self.head
        while current:
            books.append(current.data)
            current = current.next
        return books

    def search_books(self, keyword):
        results = []
        current = self.head
        while current:
            book = current.data
            if (
                keyword.lower() in book["title"].lower()
                or keyword.lower() in book["author"].lower()
                or keyword.lower() in book["isbn"].lower()
                or keyword.lower() in book["year"].lower()
            ):
                results.append(book)
            current = current.next
        return results

    def delete_book(self, isbn):
        current = self.head
        previous = None
        while current:
            if current.data["isbn"] == isbn:
                if previous:
                    previous.next = current.next
                else:
                    self.head = current.next
                return True
            previous = current
            current = current.next
        return False

-
class LibrarySystem:
    def __init__(self, master):
        self.master = master
        self.master.title("Library System (Linked List)")
        self.master.geometry("700x500")
        self.library = LinkedList()

        # --- Frames ---
        self.frame_input = tk.Frame(master, padx=10, pady=10)
        self.frame_input.pack(fill="x")

        self.frame_buttons = tk.Frame(master, padx=10, pady=10)
        self.frame_buttons.pack(fill="x")

        self.frame_table = tk.Frame(master, padx=10, pady=10)
        self.frame_table.pack(fill="both", expand=True)

        # --- Input fields ---
        tk.Label(self.frame_input, text="Title:").grid(row=0, column=0)
        tk.Label(self.frame_input, text="Author:").grid(row=0, column=2)
        tk.Label(self.frame_input, text="Year:").grid(row=1, column=0)
        tk.Label(self.frame_input, text="ISBN:").grid(row=1, column=2)

        self.title_entry = tk.Entry(self.frame_input)
        self.author_entry = tk.Entry(self.frame_input)
        self.year_entry = tk.Entry(self.frame_input)
        self.isbn_entry = tk.Entry(self.frame_input)

        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        self.author_entry.grid(row=0, column=3, padx=5, pady=5)
        self.year_entry.grid(row=1, column=1, padx=5, pady=5)
        self.isbn_entry.grid(row=1, column=3, padx=5, pady=5)

        # --- Buttons ---
        tk.Button(self.frame_buttons, text="Add Book", command=self.add_book).pack(side="left", padx=5)
        tk.Button(self.frame_buttons, text="View All", command=self.view_all).pack(side="left", padx=5)
        tk.Button(self.frame_buttons, text="Search", command=self.search_book).pack(side="left", padx=5)
        tk.Button(self.frame_buttons, text="Delete", command=self.delete_book).pack(side="left", padx=5)
        tk.Button(self.frame_buttons, text="Exit", command=master.quit).pack(side="right", padx=5)

       
        columns = ("Title", "Author", "Year", "ISBN")
        self.tree = ttk.Treeview(self.frame_table, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(fill="both", expand=True)


    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        year = self.year_entry.get().strip()
        isbn = self.isbn_entry.get().strip()

        if not title or not author or not year or not isbn:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        book = {"title": title, "author": author, "year": year, "isbn": isbn}
        self.library.add_book(book)
        messagebox.showinfo("Success", f"Book '{title}' added successfully!")
        self.clear_entries()
        self.view_all()

    def view_all(self):
        self.tree.delete(*self.tree.get_children())
        books = self.library.get_all_books()
        for book in books:
            self.tree.insert("", "end", values=(book["title"], book["author"], book["year"], book["isbn"]))

    def search_book(self):
        keyword = self.title_entry.get().strip()
        if not keyword:
            messagebox.showwarning("Input Error", "Please enter a keyword to search.")
            return
        results = self.library.search_books(keyword)
        self.tree.delete(*self.tree.get_children())
        for book in results:
            self.tree.insert("", "end", values=(book["title"], book["author"], book["year"], book["isbn"]))

    def delete_book(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a book to delete.")
            return
        isbn = self.tree.item(selected_item)["values"][3]
        deleted = self.library.delete_book(isbn)
        if deleted:
            messagebox.showinfo("Success", "Book deleted successfully!")
            self.view_all()
        else:
            messagebox.showerror("Error", "Book not found.")

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.isbn_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = LibrarySystemUI(root)
    root.mainloop()

