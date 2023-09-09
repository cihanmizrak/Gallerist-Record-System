import sqlite3
import tkinter as tk
from tkinter import ttk

# Create an SQLite database
conn = sqlite3.connect("gallery.db")
cursor = conn.cursor()

# Create Galeri, Kullanici, and Arac tables if they don't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS Galeri (
                    id INTEGER PRIMARY KEY,
                    gallery_name TEXT,
                    address TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Kullanici (
                    id INTEGER PRIMARY KEY,
                    first_name TEXT,
                    last_name TEXT,
                    username TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Arac (
                    id INTEGER PRIMARY KEY,
                    brand TEXT,
                    model TEXT,
                    year INTEGER,
                    gallery_id INTEGER,
                    user_id INTEGER,
                    FOREIGN KEY (gallery_id) REFERENCES Galeri(id),
                    FOREIGN KEY (user_id) REFERENCES Kullanici(id))''')

conn.commit()

class Galeri:
    def __init__(self, gallery_name, address):
        self.gallery_name = gallery_name
        self.address = address
        self.id = None

    def save(self):
        cursor.execute("INSERT INTO Galeri (gallery_name, address) VALUES (?, ?)",
                       (self.gallery_name, self.address))
        self.id = cursor.lastrowid
        conn.commit()

class Kullanici:
    def __init__(self, first_name, last_name, username):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.id = None

    def save(self):
        cursor.execute("INSERT INTO Kullanici (first_name, last_name, username) VALUES (?, ?, ?)",
                       (self.first_name, self.last_name, self.username))
        self.id = cursor.lastrowid
        conn.commit()

class Arac:
    def __init__(self, brand, model, year, gallery, user):
        self.brand = brand
        self.model = model
        self.year = year
        self.gallery = gallery
        self.user = user
        self.id = None

    def save(self):
        cursor.execute("INSERT INTO Arac (brand, model, year, gallery_id, user_id) VALUES (?, ?, ?, ?, ?)",
                       (self.brand, self.model, self.year, self.gallery.id, self.user.id))
        self.id = cursor.lastrowid
        conn.commit()

# Tkinter GUI
def add_gallery():
    gallery_name = gallery_name_entry.get()
    address = address_entry.get()
    new_gallery = Galeri(gallery_name, address)
    new_gallery.save()
    refresh_listboxes()

def add_user():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    username = username_entry.get()
    new_user = Kullanici(first_name, last_name, username)
    new_user.save()
    refresh_listboxes()

def add_vehicle():
    brand = brand_entry.get()
    model = model_entry.get()
    year = year_entry.get()
    selected_gallery = gallery_listbox.get(gallery_listbox.curselection())
    selected_user = user_listbox.get(user_listbox.curselection())

    # Find the corresponding gallery and user objects
    gallery_object = [gallery for gallery in galleries if gallery.gallery_name == selected_gallery][0]
    user_object = [user for user in users if user.username == selected_user][0]

    new_vehicle = Arac(brand, model, year, gallery_object, user_object)
    new_vehicle.save()
    refresh_listboxes()

def refresh_listboxes():
    gallery_listbox.delete(0, tk.END)
    user_listbox.delete(0, tk.END)

    for gallery in galleries:
        gallery_listbox.insert(tk.END, gallery.gallery_name)

    for user in users:
        user_listbox.insert(tk.END, user.username)

# Initialize Tkinter
root = tk.Tk()
root.title("Gallery Management System")

# Gallery Entry Widgets
gallery_frame = ttk.Frame(root)
gallery_frame.grid(row=0, column=0, padx=10, pady=10)

gallery_label = ttk.Label(gallery_frame, text="Gallery Name:")
gallery_label.grid(row=0, column=0, sticky="w")

gallery_name_entry = ttk.Entry(gallery_frame)
gallery_name_entry.grid(row=0, column=1, padx=5)

address_label = ttk.Label(gallery_frame, text="Address:")
address_label.grid(row=1, column=0, sticky="w")

address_entry = ttk.Entry(gallery_frame)
address_entry.grid(row=1, column=1, padx=5)

add_gallery_button = ttk.Button(gallery_frame, text="Add Gallery", command=add_gallery)
add_gallery_button.grid(row=2, columnspan=2, pady=5)

# User Entry Widgets
user_frame = ttk.Frame(root)
user_frame.grid(row=0, column=1, padx=10, pady=10)

user_label = ttk.Label(user_frame, text="Username:")
user_label.grid(row=0, column=0, sticky="w")

username_entry = ttk.Entry(user_frame)
username_entry.grid(row=0, column=1, padx=5)

first_name_label = ttk.Label(user_frame, text="First Name:")
first_name_label.grid(row=1, column=0, sticky="w")

first_name_entry = ttk.Entry(user_frame)
first_name_entry.grid(row=1, column=1, padx=5)

last_name_label = ttk.Label(user_frame, text="Last Name:")
last_name_label.grid(row=2, column=0, sticky="w")

last_name_entry = ttk.Entry(user_frame)
last_name_entry.grid(row=2, column=1, padx=5)

add_user_button = ttk.Button(user_frame, text="Add User", command=add_user)
add_user_button.grid(row=3, columnspan=2, pady=5)

# Vehicle Entry Widgets
vehicle_frame = ttk.Frame(root)
vehicle_frame.grid(row=0, column=2, padx=10, pady=10)

brand_label = ttk.Label(vehicle_frame, text="Brand:")
brand_label.grid(row=0, column=0, sticky="w")

brand_entry = ttk.Entry(vehicle_frame)
brand_entry.grid(row=0, column=1, padx=5)

model_label = ttk.Label(vehicle_frame, text="Model:")
model_label.grid(row=1, column=0, sticky="w")

model_entry = ttk.Entry(vehicle_frame)
model_entry.grid(row=1, column=1, padx=5)

year_label = ttk.Label(vehicle_frame, text="Year:")
year_label.grid(row=2, column=0, sticky="w")

year_entry = ttk.Entry(vehicle_frame)
year_entry.grid(row=2, column=1, padx=5)

gallery_label = ttk.Label(vehicle_frame, text="Select Gallery:")
gallery_label.grid(row=3, column=0, sticky="w")

gallery_listbox = tk.Listbox(vehicle_frame, selectmode = tk.SINGLE, width=20)
gallery_listbox.grid(row=3, column=1, padx=5)

user_label = ttk.Label(vehicle_frame, text="Select User:")
user_label.grid(row=4, column=0, sticky="w")

user_listbox = tk.Listbox(vehicle_frame, selectmode=tk.SINGLE, width=20)
user_listbox.grid(row=4, column=1, padx=5)

add_vehicle_button = ttk.Button(vehicle_frame, text="Add Vehicle", command=add_vehicle)
add_vehicle_button.grid(row=5, columnspan=2, pady=5)

# Load existing data
galleries = [Galeri(*row) for row in cursor.execute("SELECT * FROM Galeri").fetchall()]
users = [Kullanici(*row) for row in cursor.execute("SELECT * FROM Kullanici").fetchall()]

refresh_listboxes()

root.mainloop()

# Close the database
conn.close()
