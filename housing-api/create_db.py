import psycopg2 as psycopg


# create the database
conn = psycopg.connect(database="postgres", user="postgres", password="your_password", host="127.0.0.1", port="5432")
conn.autocommit = True
cur = conn.cursor()
# checking if it exists or creating it
cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", ('house',))
exists = cur.fetchone()
if not exists:
    cur.execute('CREATE DATABASE house;')
    print("Database 'house' created successfully!")

elif exists:
    print("The database already exists")

cur.close()
conn.close()
