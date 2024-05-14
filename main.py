from flask  import  Flask,render_template,redirect,url_for,request,session,flash
from database import get_data,insert_products,insert_sales,check_email_exists,insert_user,check_email_password,update_products

app =  Flask(__name__)
app.secret_key ='fjfkfifii4848v'


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/products')
def products():
    if 'email' not in session:
        return redirect(url_for('login'))
    products = get_data('products')
    return render_template('products.html',products=products)


@app.route('/contact')
def contact():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template('contact.html')

@app.route('/sales')
def sales():
    if 'email' not in session:
        return redirect(url_for('login'))
    sales = get_data('sales')
    products = get_data('products')
    return render_template('sales.html',sales = sales,products=products)

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == "POST":
        f_name = request.form['f_name']
        email = request.form['email']
        password = request.form['pass']
        #check if email exists
        check_email =check_email_exists(email)
        #INSERT NEW USER
        if check_email == None:
            new = (f_name,email,password)
            insert_user(new)
            return redirect(url_for('login'))
        else:
            flash('Email exists')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/login',methods = ['GET','POST'])
def login():
    #GET FORM DATA
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        #CHECK EMAIL EXISTS
        check = check_email_exists(email)
        if check == None:
            return redirect(url_for('register'))
        else:
            #CROSSCHECK PASSWORD AGAINST EMAIL
            ch = check_email_password(email,password)
            if len(ch) < 1:
                flash('Incorrect email or password')
            else:
                #STORE EMAIL IN A SESSION
                session['email']= email
                return redirect(url_for('dashboard'))
        
    return render_template('login.html')

@app.route('/add_prods', methods=['GET','POST'] )
def add_prods():
    p_name = request.form['name']
    b_price = request.form['buying']
    s_price = request.form['selling']
    stock = request.form['stock']
    new = (p_name,b_price,s_price,stock)
    insert_products(new)
    return redirect(url_for('products'))

@app.route('/update_prods',methods=['GET','POST'])
def update_prods():

    pid = request.form['select']
    buying = request.form['buying']
    selling = request.form['selling']
    stock = request.form['stock']
    new = (buying,selling,stock)
    update_products(new,pid)
    return redirect(url_for('products'))

@app.route('/make_sale',methods=['GET','POST'])
def make_sale():
    pid = request.form['select']
    quantity = request.form['quantity']
    new = (pid,quantity)
    insert_sales(new)
    flash('Sale made successfully')
    return redirect(url_for('sales'))

@app.route('/logout')
def log_out():
    session.pop('email',None)
    return redirect(url_for('login'))


app.run(debug=True)