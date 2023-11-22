import sqlite3
import unicodecsv as csv

# Create a new SQLite database or connect if it already exists
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Drop the table if it already exists
cursor.execute("DROP TABLE IF EXISTS history;")

# Create the table
create_table_query = """
    create table history (
	    id INTEGER
		    constraint history_pk
			    primary key autoincrement,
	    target INTEGER not null
		    constraint history_products_id_fk
			    references products,
	    amount INTEGER not null
    );
"""
cursor.execute(create_table_query)

# Commit changes and close the connection
conn.commit()
conn.close()
