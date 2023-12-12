import sqlite3
import unicodecsv as csv

# Path to your CSV file
csv_file_path = 'data.csv'  # Replace with your CSV file path

# Create a new SQLite database or connect if it already exists
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Drop the table if it already exists
cursor.execute("DROP TABLE IF EXISTS products;")

# Create the table
create_table_query = """
    CREATE TABLE products (
        id INTEGER PRIMARY KEY,
        rank INTEGER,
        name TEXT,
        amount INTEGER,
        isShow INTEGER default 0
    );
"""
cursor.execute(create_table_query)


# Function to convert rank text to number
def convert_rank(rank_text):
    rank_mapping = {'ur': 4, 'sr': 3, 'sp': 2, 'r': 1}
    return rank_mapping.get(rank_text.lower(), 0)  # Default to 0 if rank is not recognized


# Read the CSV file and insert data into the SQLite database
with open(csv_file_path, 'rb') as csv_file:  # Open in binary mode
    csv_reader = csv.reader(csv_file, encoding='utf-8')
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        row[1] = convert_rank(row[1])  # Convert rank text to number
        row = row[:4]
        print(row)
        cursor.execute("INSERT INTO products (id, rank, name, amount) VALUES (?, ?, ?, ?);", row)

# Commit changes and close the connection
conn.commit()
conn.close()
