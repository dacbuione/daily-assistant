import sqlite3

# Initialize database and tables (if they do not exist)
def init_db():
    conn = sqlite3.connect('assistants.db')
    cursor = conn.cursor()

    # Create user_info table if it does not exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_info (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        weight REAL,
                        height REAL,
                        water_intake REAL,
                        health_goal TEXT)''')

    # Create health_info table if it does not exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS health_info (
                        id INTEGER PRIMARY KEY,
                        content TEXT)''')

    conn.commit()
    conn.close()

# Insert user information into the table
def insert_user_info(weight, height, health_goal):
    water_intake = calculate_water_intake(weight, height)
    conn = sqlite3.connect('assistants.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO user_info (weight, height, water_intake, health_goal) VALUES (?, ?, ?, ?)''', 
                   (weight, height, water_intake, health_goal))
    conn.commit()
    conn.close()

# Calculate water intake based on weight and height
def calculate_water_intake(weight, height):
    water_intake = weight * 35  # Simple formula: drink about 35ml of water for each kg of weight
    return water_intake

# Get user information from the table
def get_user_info():
    conn = sqlite3.connect('assistants.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_info")
    user_info = cursor.fetchall()
    conn.close()
    return user_info

# Store health data in the database
def store_data_in_db(data):
    conn = sqlite3.connect('assistants.db')
    cursor = conn.cursor()
    for item in data:
        cursor.execute('INSERT INTO health_info (content) VALUES (?)', (item,))
    conn.commit()
    conn.close()
