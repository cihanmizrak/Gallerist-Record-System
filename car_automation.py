import sqlite3

# Create an SQLite database
conn = sqlite3.connect("gallery.db")
cursor = conn.cursor()

# Create Galeri, Kullanici, and Arac tables
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
        self.id = None  # Primary key (id) attribute for the Galeri object

    def save(self):
        cursor.execute("INSERT INTO Galeri (gallery_name, address) VALUES (?, ?)",
                       (self.gallery_name, self.address))
        self.id = cursor.lastrowid  # Get the id of the created record
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

# Add sample data
gallery1 = Galeri("Sample Gallery 1", "123 Example Street, Istanbul")
gallery1.save()

user1 = Kullanici("Ahmet", "Yılmaz", "ahmet_123")
user1.save()

vehicle1 = Arac("Toyota", "Corolla", 2022, gallery1, user1)
vehicle1.save()

# Retrieve data from the database:
cursor.execute("SELECT * FROM Galeri")
gallery_data = cursor.fetchall()
print("Gallery Data:")
for data in gallery_data:
    print(data)

cursor.execute("SELECT * FROM Kullanici")
user_data = cursor.fetchall()
print("\nUser Data:")
for data in user_data:
    print(data)

cursor.execute("SELECT * FROM Arac")
vehicle_data = cursor.fetchall()
print("\nVehicle Data:")
for data in vehicle_data:
    print(data)

# Close the database
conn.close()

