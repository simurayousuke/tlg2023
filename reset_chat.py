import sqlite3
import unicodecsv as csv

# Create a new SQLite database or connect if it already exists
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Drop the table if it already exists
cursor.execute("DROP TABLE IF EXISTS chat;")

# Create the table
create_table_query = """
	create table chat (
		id INTEGER
			constraint chat_pk
				primary key autoincrement,
		comment TEXT not null,
		time datetime default current_timestamp not null
	);
"""
cursor.execute(create_table_query)

# Commit changes and close the connection
conn.commit()
conn.close()
