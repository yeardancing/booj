import sqlite3

class BoojDb():
    def __init__(self, dbName):
        self.dbName = dbName
        self.conn = sqlite3.connect(dbName)
        self.c = conn.cursor()
        sql = 'create table if not exists songs 
                (id INTEGER NOTNULL,
                 artist VARCHAR(64) NOT NULL,
                 title VARCHAR(64) NOT NULL,
                 album VARCHAR(64) NOT NULL,
                 filename VARCHAR(64) NOT NULL)'
        c.execute(sql)

    def rebuildDatabase(self):
        

# Create table
c.execute('''CREATE TABLE stocks
             (date text, trans text, symbol text, qty real, price real)''')

# Insert a row of data
c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

The data you’ve saved is persistent and is available in subsequent sessions:

import sqlite3
conn = sqlite3.connect('example.db')
c = conn.cursor()

Usually your SQL operations will need to use values from Python variables. You 
shouldn’t assemble your query using Python’s string operations because doing so 
is insecure; it makes your program vulnerable to an SQL injection attack 
(see http://xkcd.com/327/ for humorous example of what can go wrong).

Instead, use the DB-API’s parameter substitution. Put ? as a placeholder wherever 
you want to use a value, and then provide a tuple of values as the second argument 
to the cursor’s execute() method. (Other database modules may use a different 
placeholder, such as %s or :1.) For example:

# Never do this -- insecure!
symbol = 'RHAT'
c.execute("SELECT * FROM stocks WHERE symbol = '%s'" % symbol)

# Do this instead
t = ('RHAT',)
c.execute('SELECT * FROM stocks WHERE symbol=?', t)
print c.fetchone()

# Larger example that inserts many records at a time
purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
             ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
             ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
            ]
c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)

To retrieve data after executing a SELECT statement, you can either treat the 
cursor as an iterator, call the cursor’s fetchone() method to retrieve a single 
matching row, or call fetchall() to get a list of the matching rows.

This example uses the iterator form:
>>>
>>> for row in c.execute('SELECT * FROM stocks ORDER BY price'):
print row

(u'2006-01-05', u'BUY', u'RHAT', 100, 35.14)
(u'2006-03-28', u'BUY', u'IBM', 1000, 45.0)
(u'2006-04-06', u'SELL', u'IBM', 500, 53.0)
(u'2006-04-05', u'BUY', u'MSFT', 1000, 72.0)
'''
