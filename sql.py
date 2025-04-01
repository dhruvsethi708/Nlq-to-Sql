import sqlite3

conn = sqlite3.connect('database.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS demo (
                name TEXT, 
                email TEXT, 
                password TEXT, 
                runs INTEGER, 
                wins INTEGER, 
                losses INTEGER, 
                ties INTEGER, 
                centuries INTEGER
            )''')


c.execute("INSERT INTO demo (name, email, password, runs, wins, losses, ties, centuries) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
  ('Virat', 'virat.kohli@gmail.com', 'virat', 10000, 18, 12, 0, 82))

c.execute("INSERT INTO demo (name, email, password, runs, wins, losses, ties, centuries) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
  ('Dhoni', 'ms@dhoni.com', 'dhoni', 7000, 20, 5, 0, 15))

c.execute("INSERT INTO demo (name, email, password, runs, wins, losses, ties, centuries) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
  ('Rohit', 'rohit@sharma.com', 'rohit', 8000, 17, 10, 0, 50))

print("The inserted records are ")
# Query the database
data = c.execute("SELECT * FROM demo")

for row in data:
    print(row)  

# close the connection
conn.commit()
conn.close()
