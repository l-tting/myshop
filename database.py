import psycopg2

#connecting to postgressql database
conn = psycopg2.connect(
    dbname = 'magnus',
    user = 'postgres',
    password = '6979',
    host = 'localhost',
    port = 5432
)
# open a cursor to perform database operation

cur = conn.cursor()

def get_data(table):
    query = f'select * from {table}'
    cur.execute(query)
    data = cur.fetchall()
    return data

def insert_products(values):
    query = f'insert into products(name,buying_price,selling_price,stock_quantity)values{values}'
    cur.execute(query)
    conn.commit()
 
def update_products(values, name):
    query = 'UPDATE products SET buying_price = %s, selling_price = %s, stock_quantity = %s  WHERE name = %s'
    cur.execute(query, (values[0], values[1], values[2], name))
    conn.commit()


def insert_sales(values):
    query = 'insert into sales(pid,quantity,created_at)values(%s,%s,now())'
    cur.execute(query,values)
    conn.commit()

def insert_user(values):
    query = 'insert into users(full_name,email,password)values(%s,%s,%s)'
    cur.execute(query,values)
    conn.commit()

def check_email_exists(email):
    query = 'select * from users  where email = %s'
    cur.execute(query,(email,))
    data = cur.fetchone()
    return data

def check_email_password(email,password):
    query = 'select * from users where email=%s and password=%s'
    cur.execute(query,(email,password))
    data = cur.fetchall()
    return data
