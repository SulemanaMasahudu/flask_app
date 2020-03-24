from flask import Flask, render_template, url_for, request, flash, redirect
from flask_bootstrap import Bootstrap
from flask import jsonify
from forms import RegistrationForm,AddEmployeePayroll,DeductFromAnEmployee,DeductAllPayroll,AddHouseCashForm,LoginForm, AddLundryItem,RequestResetForm,ResetPasswordForm, AddCashForm, AddExpenseForm, AddNewCustomer, AddNewAsset, AddEmployee
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.sql import func
from sqlalchemy import exc, extract
from datetime import date
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Mail, Message
import os
import tempfile
from escpos.printer import Network
from num2words import num2words
import cv2
from PIL import Image



app = Flask(__name__)
Bootstrap(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

app.config['SECRET_KEY'] = '1234retdheyetet343536gsgsgsgdhdh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'smasahudu97@gmail.com'#os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = 'watchme100'#os.environ.get('EMAIL_PASS')
mail = Mail(app)




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#CREATING DATABASE TABLE FOR APPLICATION USERS 
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable=False)
    email = db.Column(db.String(120), unique = True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default= 'default.jpg')
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, nullable= False, default = datetime.utcnow)
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)    
    
    
#DATABASE TABEL FOR UNDER LAUNDRY SERVICE  CUSTOMERS
class Customers(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    customer_name = db.Column(db.String(20),  nullable=False)
    location = db.Column(db.String(20),  nullable=False)
    phone = db.Column(db.Integer,  nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    service = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer,  nullable=False,)
    #items = db.relationship('Cashitems', backref = 'customer', lazy=True)
    date_created = db.Column(db.DateTime, nullable= False, default = datetime.utcnow)
    
   
    def as_dict(self):
        return {'customer_name': self.customer_name}
    
#MAKING AJAX REQUEST TO PULL OUT CUSTOMERS
@app.route('/customer2')
def customer2():
	res = Customers.query.all()
	list_customers = [r.as_dict() for r in res]
	return jsonify(list_customers)

#DATABASE TABLE FOR CASH ITEMS  laundry service
class Cashitems(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    customer_name = db.Column(db.String(100),  nullable=False)
    item_name = db.Column(db.String(20),  nullable=False)
    quantity = db.Column(db.Integer,  nullable=False)
    price = db.Column(db.Integer,  nullable=False)
    total = db.Column(db.Integer,  nullable=False)
    user_id = db.Column(db.Integer,   nullable=False,)
    paid = db.Column(db.Integer,   nullable=True,)
    date_created = db.Column(db.DateTime, nullable= False, default = datetime.utcnow)
    
    def as_dict(self):
        
        return {'id':self.id,'customer_name':self.customer_name, 'item_description': self.item_name, 'amount':self.total, 'date':self.date_created}

#DATABASE TABLE FOR HOUSE KEEPING CASH ENTRY

class HouseCashitems(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    customer_name = db.Column(db.String(100),  nullable=False)
    item_name = db.Column(db.String(20),  nullable=False)
    quantity = db.Column(db.Integer,  nullable=False)
    price = db.Column(db.Integer,  nullable=False)
    total = db.Column(db.Integer,  nullable=False)
    user_id = db.Column(db.Integer,   nullable=False,)
    paid = db.Column(db.Integer,   nullable=True,)
    date_created = db.Column(db.DateTime, nullable= False, default = datetime.utcnow)
    
    def as_dict(self):
        
        return {'id':self.id,'customer_name':self.customer_name, 'item_description': self.item_name, 'amount':self.total, 'date':self.date_created}

 
#DATABASE 4 EXPENSES MADE OR INCURED BY COMPANY    
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    category = db.Column(db.String(120),  nullable=False)
    description = db.Column(db.String(120),  nullable=False)
    amount = db.Column(db.Integer,  nullable=False)
    expense_type = db.Column(db.String(30),  nullable=False)
    #items = db.relationship('Cashitems', backref = 'customer', lazy=True)
    date_created = db.Column(db.DateTime, nullable= False, default = datetime.utcnow)
    
#DATABASE FOR EMPLOYEES OF COMPANY
class Employees(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String(120),  nullable=False)
    contact = db.Column(db.String(120),  nullable=False)
    digital_address = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    position = db.Column(db.String(120), nullable=False)
    salary = db.Column(db.String(30),  nullable=False)
    employee_type = db.Column(db.String(30), nullable=False)
    gender = db.Column(db.String(30), nullable=False)
    date_created = db.Column(db.DateTime, nullable= False, default = datetime.utcnow)
    
    def as_dict(self):
        return {'employee_name': self.name,'employee_type':self.employee_type, 'employee_position':self.position, 'employee_id':self.id, 'employee_amount':self.salary}
    
    
#MAKING AJAX REQUEST TO PULL OUT Employees
@app.route('/pullemployees')
def pullemployees():
	res = Employees.query.all()
	list_customers = [r.as_dict() for r in res]
	return jsonify(list_customers)    
 
#DATABASE FOR COMPANY ASSETS    
class Company_assets(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String(120),  nullable=False)
    producers = db.Column(db.String(120),  nullable=False)
    code = db.Column(db.Integer,  nullable=False)
    year_purchased = db.Column(db.String(120), nullable=False)
    date_created = db.Column(db.DateTime, nullable= False, default = datetime.utcnow)
    
    
#SALARY TABLE   
class Employee_Salary(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String(240),  nullable=False)
    user_id = db.Column(db.Integer,  nullable=True)
    position = db.Column(db.String(240),  nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    which_work = db.Column(db.String(240),  nullable=False)
    date_paid = db.Column(db.DateTime, nullable= False, default = datetime.utcnow)
    
#EMPLOYEE SALARY DEDUCTION TABLE   
class Employee_Deduction(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    employee_id = db.Column(db.Integer,  nullable=False)
    employee_name = db.Column(db.String(240),  nullable=False)
    employee_position = db.Column(db.String(240),  nullable=False)
    employee_category = db.Column(db.String(240),  nullable=False)
    about_deduction = db.Column(db.String(240),  nullable=False)
    amount_deducted = db.Column(db.Integer, nullable=False)
    date_paid = db.Column(db.DateTime, nullable= False, default = datetime.utcnow)    
        
 #TABLE FOR RECEIPTS   
class Receipts(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String(240),  nullable=False)  
    type_of_receipt = db.Column(db.String(240),  nullable=False)
    date_created = db.Column(db.DateTime, nullable= False, default = datetime.utcnow)    
    
#ADD  ITEM PRICE TO DATABASE
class Lundry_prices(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    item_name = db.Column(db.String(120),  nullable=False)
    price = db.Column(db.String(120),  nullable=False)
    date_created = db.Column(db.DateTime, nullable= False, default = datetime.utcnow)
    
    def as_dict(self):
        
        return {'item_name': self.item_name, 'price':self.price}

#AJAX ROUTE TO RETRIEVE LAUNDRY ITEM PRICES AND NAMES
@app.route('/myitems')
def myitems():
	res = Lundry_prices.query.all()
	list_items = [r.as_dict() for r in res]
	return jsonify(list_items)    

#AJAX REQUEST TO RETRIEVE TRANSACTIONS
@app.route('/trans')
def trans():
	res = Cashitems.query.all()
	list_trans= [r.as_dict() for r in res]
	return jsonify(list_trans)    

#AJAX REQUEST TO RETRIEVE ALL HOUSE KEEPINGTRANSACTIONS
@app.route('/Housetrans')
def Housetrans():
	res = HouseCashitems.query.all()
	list_trans= [r.as_dict() for r in res]
	return jsonify(list_trans)    

#**********ROUTE FOR INDEX PAGE FROM LOGIN PAGE***********
@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('about'))
        else:
            flash('Login Unsucessful, please check username and password', 'danger')
             
    return render_template('login.html', title='login', form=form)


#*************LOGIN PAGE AND LOGIN PROCESS****************
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('about'))
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('about'))
        else:
            flash('Login Unsucessful, please check username and password', 'danger')
            
    return render_template('login.html', title='login', form=form)


#function to print receipt
def iprint(itemtoprint):
    try:
        kitchen = Network("192.168.1.100")
        filename = open(itemtoprint, 'r')
        kitchen.text(filename)
        kitchen.cut()
    except OSError:
        pass   
    
    
#***********ROUTE TO LAUNDRYry TRANSACTION PAGE AND AADDING A NEW TRANSACTION***********!!!    
@login_required
@app.route('/transactions', methods=['GET','POST'])
def transactions():
    form = AddCashForm()     
    if form.validate_on_submit():
        cashit = Cashitems(
             customer_name = form.customer_name.data,
             item_name = form.itemname.data,
             quantity = form.quantity.data,
             price = form.price.data,
             total = form.total.data,
             user_id = current_user.id
        )
      
        db.create_all()
        db.session.add(cashit)
        db.session.commit()
        flash('Successful', 'success')
        try:
            os.makedirs("C:/Users/Mashud/Desktop/FLASK_CMS/static/Entry_receipts")
            os.chdir("C:/Users/Mashud/Desktop/FLASK_CMS/static/Entry_receipts")
        except FileExistsError:
            os.chdir("C:/Users/Mashud/Desktop/FLASK_CMS/static/Entry_receipts")    
        name = form.customer_name.data + str(datetime.now().strftime("%H%M%S")) + '.jpg'
        filename = 'C:/Users/Mashud/Desktop/flask_cms/static/logo.jpg'
        #os.system(filename)
        image = cv2.imread(filename)
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(name,image_gray)     
        

        with open(name, 'a') as f:
            f.write(f'''
                    
                    
                    *********************************************************************
                    *********************************************************************
                    Date: {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}               *
                    Name: {form.customer_name.data}\n                                   *
                    Item Description: {form.itemname.data}\n                            *
                    Quantity: {form.quantity.data}\n                                    *
                    Price: {form.total.data}     
                                                    *
                                                                                        *
                    *********************************************************************
                    ''')
            
            
            receipt = Receipts(
             name = name,
             type_of_receipt = 'Lr',
              )
            db.session.add(receipt)
            db.session.commit()
            iprint(name)
    items = Cashitems.query.all()
    return render_template('transactions.html', form= form, items=items)

@app.route('/laundry_receipts')
def laundry_receipts():
    receipts = Receipts.query.filter_by(type_of_receipt='Lr').all()
    folder = 'Entry_receipts'
    return render_template('receipts.html', receipts=receipts, folder=folder) 

#RETRIEVE MONTHLY AVAILABLE PAYSLIPS
@app.route('/payslips_per_month')
def payslips_per_month():
    receipts = Receipts.query.filter(
                    extract('month', Receipts.date_created) ==  datetime.today().month,
                    Receipts.type_of_receipt == 'Ps').all()
    return render_template('payslips.html', receipts=receipts) 



#***********ROUTE TO HOUSE KEEPING TRANSACTION PAGE AND AADDING A NEW TRANSACTION***********!!!    
@login_required
@app.route('/house_transactions', methods=['GET','POST'])
def House_transactions():
    form = AddHouseCashForm()     
    if form.validate_on_submit():
        cashit = HouseCashitems(
             customer_name = form.customer_name.data,
             item_name = form.itemname.data,
             quantity = form.quantity.data,
             price = form.price.data,
             total = form.total.data,
             user_id = current_user.id
        )
        
        db.create_all()
        db.session.add(cashit)
        db.session.commit()
        flash('Successful', 'success')
        try:
            os.makedirs("C:/Users/Mashud/Desktop/FLASK_CMS/static/Entry_receipts")
            os.chdir("C:/Users/Mashud/Desktop/FLASK_CMS/static/Entry_receipts")
        except FileExistsError:
            os.chdir("C:/Users/Mashud/Desktop/FLASK_CMS/static/Entry_receipts")    
        name = form.customer_name.data + str(datetime.now().strftime("%H%M%S"))+'.pdf'
        with open(name, 'w+') as f:
            f.write(f'''
                    *********************************************************************
                    *********************************************************************
                    Date: {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}               *
                    Name: {form.customer_name.data}\n                                   *
                    Item Description: {form.itemname.data}\n                            *
                    Quantity: {form.quantity.data}\n                                    *
                    Price: {form.total.data}                                            *
                                                                                        *
                    *********************************************************************
                    ''')
            
            receipt = Receipts(
             name = name,
             type_of_receipt = 'Hr',
              )
            db.session.add(receipt)
            db.session.commit()
            iprint(name)
    items = HouseCashitems.query.all()
    return render_template('House_keeping_transactions.html', form= form, items=items)


#***********ROUTE FOR EXPENSES PAGE AND ADDING A NEW EXPENSE************
@login_required
@app.route('/expenses', methods=['GET', 'POST'])
def expenses():
    form = AddExpenseForm()
    if form.validate_on_submit():
        expen = Expense(
            category =form.category.data,
            description=form.description.data,
            amount=form.amount.data,
            expense_type = form.expense_category.data
            )
        db.session.add(expen)
        db.session.commit()
        flash('A new Expense added successfully', 'success')
        
    expenses =  Expense.query.filter_by(expense_type='L').all() 
    purchase =  Expense.query.with_entities(func.sum(Expense.amount)).filter_by(expense_type='L',category='Purchase' ).first(),
    salary = Expense.query.with_entities(func.sum(Expense.amount)).filter_by(expense_type='L',category='Salary' ).first()
    pur = purchase[0][0]
    sal = salary[0]
    values = [
                  pur, sal 
                   ] 
    
    if form.expense_category.data == 'L':
        return render_template('expenses.html', form = form, expenses=expenses, values=values)   
    elif form.expense_category.data == 'H':
         return render_template('house_keeping_expenses.html', expenses=expenses, values=values)
   
    else:
         return render_template('expenses.html', form = form, expenses=expenses, values=values) 

#***********PAY ALL EMPLOYEES************
@login_required
@app.route('/Pay_All_Employees', methods=['GET', 'POST'])
def Pay_All_Employees():
    employees = Employees.query.all()
    form = AddLundryItem()
    form2 = AddEmployeePayroll()
    form3 = DeductAllPayroll()
    form4 = DeductFromAnEmployee()
   
    for employee in employees:
        pay = Employee_Salary(
                name = employee.name,
                user_id = employee.id,
                position = employee.position,
                salary = employee.salary,
                which_work = employee.employee_type,
                
            )
        db.session.add(pay)
        db.session.commit()
            
        flash('All Employees paid successfully', 'success')
                  
             
    return render_template('setting.html', form=form, form2=form2, form3=form3, form4=form4)


#PAY INDIVIDUAL EMPLOYEE
@app.route('/Pay_Individual_Employee', methods=['GET', 'POST'])
def Pay_Individual_Employee():
    if request.method == 'GET':
        form =  AddEmployeePayroll()
        type = 'hidden'
        return render_template('setting2.html', form=form, type=type)
    
    if request.method == 'POST':
        #form = AddEmployeePayroll()
        form2 = AddEmployeePayroll()
        form = AddLundryItem()
        form3 = DeductAllPayroll()
        form4 = DeductFromAnEmployee()
        if form2.validate_on_submit():
            print(request.form.get('user_id'))
            
            mypay = Employee_Salary(                   
                name = form2.name.data,
                user_id = form2.user_id.data,    #form2.user_id.data,
                position = form2.position.data,
                salary = form2.salary.data,
                which_work= form2.which_work.data, )
            
            #db.create_all()
            db.session.add(mypay)
            db.session.commit()
            flash('An Employee paid successfully ', 'info')
    return render_template('setting.html', form=form, form2=form2, form3=form3, form4=form4)    
                
#***********DEDUCT FROM  ALL EMPLOYEES************
@login_required
@app.route('/Deduct_All_Employees', methods=['GET', 'POST'])
def Deduct_All_Employees():
    myemployees = Employees.query.all()
    form = AddLundryItem()
    form2 = AddEmployeePayroll()
    form3 = DeductAllPayroll()
    form4 = DeductFromAnEmployee()
    for myemployee in myemployees:
        if form3.validate_on_submit():
            deduct = Employee_Deduction(
                employee_id = myemployee.id,
                employee_name = myemployee.name,
                employee_position = myemployee.position,
                employee_category = myemployee.employee_type,
                about_deduction = form3.about_deduction.data,
                amount_deducted = form3.amount_deducted.data
            )
            db.session.add(deduct)
            db.session.commit()
            
            flash('Deduction made successfully On Salaries of all workers', 'danger')
    return render_template('setting.html', form=form, form2=form2, form3 =form3, form4=form4)
#DEDUCT FROM SINGLE EMPLOYEE
@app.route('/Deduct_Indivi_Employee', methods=['GET', 'POST'])
def Deduct_Indivi_Employee():
    form = AddLundryItem()
    form2 = AddEmployeePayroll()
    form3 = DeductAllPayroll()
    form4 = DeductFromAnEmployee()
    
    if form4.validate_on_submit():
        deduct = Employee_Deduction(
                employee_id = form4.user_id.data,
                employee_name = form4.name.data,
                employee_position = form4.position.data,
                employee_category = form4.which_work.data,
                about_deduction = form4.about_deduction.data,
                amount_deducted = form4.amount_deducted.data
            )
        db.session.add(deduct)
        db.session.commit()
            
        flash('Deduction made successfully', 'danger')
    return render_template('setting.html', form=form, form2=form2, form3 =form3, form4=form4)


#*********CUSTOMERS AND ADDING A NEW CUSTOMER TO DATABASE***********!!!
@login_required
@app.route('/customers', methods=['GET', 'POST'])
def customers():
    form = AddNewCustomer()
    if form.validate_on_submit():
        custo = Customers(
            customer_name=form.customer_name.data,
            location=form.location.data,
            gender=form.gender.data,
            service=form.service.data,
            phone=form.phone.data,
            user_id = current_user.id)
        db.session.add(custo)
        db.session.commit()
        flash('New customer Added', 'success')
    customers = Customers.query.filter_by(service = 'L').all()     
    male_count = Customers.query.filter_by(gender='M', service='L').count()
    female_count =Customers.query.filter_by(gender='F', service='L').count()
    total  =  male_count + female_count
    if total > 0:
        male = round(male_count/ total * 100)
        female = round(female_count/total *100)
        return render_template('customers.html', form= form, customers=customers, male=male,female=female)
    
    return render_template('customers.html', form= form, customers=customers)


#*********ROUTE TO ACCESS COMPANY ASSETS PAGE AND ALSO ADD NEW ASSET***********!!!
@login_required
@app.route('/company_assets', methods=['GET','POST'])
def company_assets():
    form = AddNewAsset()
    if form.validate_on_submit():     
        asset = Company_assets(
            name = form.name.data,
            producers=form.producers.data,
            code = form.code.data,
            year_purchased =form.purchase_year.data,)
        db.session.add(asset)
        db.session.commit()
        flash('Asset Added successfully', 'success')
    assets = Company_assets.query.all()
    mycont = Company_assets.query.count()      
    return render_template('company_assets.html', form = form, assets = assets, mycont=mycont)


#**+++******ROUTE TO EMPLOYEE PAGE AND ADDING A NEW EMPLOYEE****++*!!!
@login_required
@app.route('/employes', methods=['GET', 'POST'])
def employes():
    if current_user.id != 1 or current_user.username !='Admin':
        return redirect(url_for('about'))
    form = AddEmployee()
    if form.validate_on_submit():
        db.create_all()
        employee = Employees(
             name=form.name.data,
             contact=form.contact.data,
             email=form.email.data,
             digital_address=form.digital_address.data,
             position = form.position.data,
             salary = form.salary.data,
             employee_type = form.which_work.data,
             gender = form.gender.data)
        db.session.add(employee)
        db.session.commit()
        flash(f'A new employee  {form.name.data} created successfully', 'success')
    employs = Employees.query.filter_by(employee_type ='L' or 'B', ).all()
    values = [
    Employees.query.filter_by(gender='M', employee_type = 'L' or 'B' ).count(),
    Employees.query.filter_by(gender='F', employee_type = 'L' or 'B' ).count()] 
    
    return render_template('employes.html', form = form, employs=employs, values=values)

#ROUTE TO REGISTRATION PAGE AND REGISTERING A NEW USER!!!!
@app.route('/register', methods =['GET','POST'])
def register():
    
    if current_user.is_authenticated and current_user.id != 1:
        return redirect(url_for('about'))
    form = RegistrationForm()
    user = User.query.filter_by(username=form.username.data).first()
    if user:
        flash(f'Username,  already exist!', 'danger')
    else:    
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash(f'Account created for {form.username.data}!, You can please Log in', 'success')
            return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)    

#++++++++++++++ROUTE TO INDEX PAGE++++++++++++++++++
@login_required
@app.route('/index')
def about():
    
    form = AddExpenseForm()
   
    mycont = Company_assets.query.count()   
    expenses =  Expense.query.count()
    total_cash =  Cashitems.query.with_entities(func.sum(Cashitems.total)).filter_by(paid=True).first(),
    total_expense = Expense.query.with_entities(func.sum(Expense.amount)).first()
    #users = User.query.all()
    tot_cash = total_cash[0][0]
    tot_expense = total_expense[0]
    values = {}
    if tot_cash is not None and tot_expense is not None:
        total_cash_and_expenses = tot_cash + tot_expense  
        cash_percent = round(tot_cash/total_cash_and_expenses * 100)
        expense_percent = round(tot_expense/total_cash_and_expenses * 100)
        
         #+++CALCULATE VALUES 4 two days ago
        for i in range(7):
             date = datetime.today()-timedelta(days=i)
             todays_date = date.strftime('%a')
             todays_of_sales =  Cashitems.query.with_entities(func.sum(Cashitems.total)).filter(
                extract('month', Cashitems.date_created) == datetime.today().month,
                extract('year', Cashitems.date_created) == datetime.today().year,
                extract('day', Cashitems.date_created) == datetime.today().day - i).all()
             twodaysago_sum = todays_of_sales [0][0]
             #values.update({'12/01/20' : 0})
             # todays_date != list(values.keys())[-1] 
             if twodaysago_sum is None:
                  values.update({todays_date: 0})
           
             elif twodaysago_sum is not None:
                  values.update({todays_date:twodaysago_sum})
                
       
            
        return render_template('index.html', form=form,mycont=mycont, values=values,cash_percent=cash_percent, expense_percent=expense_percent)
        
    mydate = datetime.today().strftime('%D')
    for i in range(7):
             date = datetime.today()-timedelta(days=i)
             todays_date = date.strftime('%a')
             todays_of_sales =  Cashitems.query.with_entities(func.sum(Cashitems.total)).filter(
                extract('month', Cashitems.date_created) == datetime.today().month,
                extract('year', Cashitems.date_created) == datetime.today().year,
                extract('day', Cashitems.date_created) == datetime.today().day - i).all()
             twodaysago_sum = todays_of_sales [0][0]
             values.update({'12/01/20' : 0})
             
             if todays_date != list(values.keys())[-1] and twodaysago_sum is None:
                  values.update({todays_date: 0})
           
             elif todays_date  != list(values.keys())[-1]  and twodaysago_sum is not None:
                  values.update({todays_date:twodaysago_sum})
    
    return render_template('index.html', mycont=mycont, values = values, form=form)

#ROUTE TO GENERATE PAYSLIP
@app.route('/payslip/<int:user_id>')
def payslip(user_id):
    employee = Employees.query.get(user_id)
    user_pay = Employee_Salary.query.with_entities(Employee_Salary.salary).filter(
                extract('month', Employee_Salary.date_paid) == datetime.today().month,
                 Employee_Salary.user_id == user_id).all()
    user_deduction = Employee_Deduction.query.with_entities(func.sum(Employee_Deduction.amount_deducted)).filter(
                extract('month', Employee_Deduction.date_paid) == datetime.today().month,
                Employee_Deduction.employee_id == user_id).all()
    
    user_deduct = Employee_Deduction.query.filter(
                extract('month', Employee_Deduction.date_paid) == datetime.today().month,
                Employee_Deduction.employee_id == user_id).all()
    masud= []
    a = len(masud)
    for item in user_deduct:
        it = str ()
        it = item.about_deduction + str(item.amount_deducted) +'\n'
        masud.append(it)
        print(item.about_deduction, item.amount_deducted)
            
    try:
        os.makedirs("C:/Users/Mashud/Desktop/FLASK_CMS/static/Entry_receipts")
        os.chdir("C:/Users/Mashud/Desktop/FLASK_CMS/static/Entry_receipts")
    except FileExistsError:
        os.chdir("C:/Users/Mashud/Desktop/FLASK_CMS/static/Entry_receipts")    
    name = employee.name + str(datetime.now().strftime("%H%M%S"))+'.TXT'
    with open(name, 'w+') as f:
        
            f.write(f'''
                    *********************************************************************
                    *********************************************************************
                    Company Name: Rodicon Ghana \n
                    Date: {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")} \n              
                    Full Name: {employee.name}\n 
                    Contact: {employee.contact}\n     
                    Email: {employee.email}\n                                    
                    Job Description: {employee.position}\n  
                    
                    EARNINGS(GHC)
                    Salary -  {user_pay[0][0]} \n \n  
                    
                    
                    DEDUCTIONS 
                    
                    {it}                                                 
                                                                        
                   ''' )
            
            receipt = Receipts(
             name = name,
             type_of_receipt = 'Ps',
              )
            db.session.add(receipt)
            db.session.commit()
             
    
    print(user_pay)
    print(user_deduction)
   
    return redirect(url_for('about'))

#ROUTE TO LOG OUT
@app.route('/logout', methods=['GET','POST'])
def logout():
    logout_user()
    return redirect('/')


#ROUTE TO LAUNDRY SUMMARY
@app.route('/laundry_summary', methods=['GET','POST'])
def laundry_summary():
    from sqlalchemy import or_
    cash =  Cashitems.query.with_entities(func.sum(Cashitems.total)).filter_by(paid=1).all(),
    mycash = cash[0][0][0]
    values = {}
    import calendar
    for i in range(1,13):
        
        monthly_customers = Customers.query.filter(
                    extract('month', Customers.date_created) == i,
                    Customers.service == 'L').count()
            
        monthly_cash = Cashitems.query.with_entities(func.sum(Cashitems.total)).filter(
                    extract('month', Cashitems.date_created) == i,
                    Cashitems.paid == 1).all()
            
        monthly_expense = Expense.query.with_entities(func.sum(Expense.amount)).filter(
                    extract('month', Expense.date_created) == i,
                    Expense.expense_type == 'L').all()
            
        if i == datetime.today().month + 1:
                break
        i = calendar.month_name[i]        
        values.update({i:[monthly_customers, monthly_cash[0][0], monthly_expense[0][0]]})    
    print(values)         
            
    if mycash is None:
        mycash = 0
    custom = Customers.query.filter_by(service = 'L').count()
    empl = Employees.query.filter(or_(Employees.employee_type == 'L', Employees.employee_type=='B')).count()
    expense = Expense.query.with_entities(func.sum(Expense.amount)).filter_by(expense_type='L').all()
    myexpense = expense[0][0]
    if myexpense is None:
        myexpense = 0
    
    if mycash > 0 and myexpense > 0:    
        total_cash= mycash + myexpense 
        mycash_percent = round(mycash/total_cash * 100) 
        myexpense_percent = round(myexpense/total_cash * 100)
    else:
        mycash_percent  = 0  
        myexpense_percent= 0      
    return render_template('laundry_summary.html',values= values,mycash_percent=mycash_percent,myexpense_percent=myexpense_percent, empl=empl,mycash=mycash,custom=custom,myexpense=myexpense)


@login_required
@app.route('/account', methods=['GET','POST'])
def account():
    return render_template('account.html', title='Account')

#ALL TRANSACTIONS PAGE
@login_required
@app.route('/alltransactions', methods=['GET','POST'])
def alltransactions():
    items = Cashitems.query.all()
    return render_template('all_transactions.html', items=items)

#ALL House keeping TRANSACTIONS PAGE
@login_required
@app.route('/allHouse_transactions', methods=['GET','POST'])
def all_Housetransactions():
    items = HouseCashitems.query.all()
    return render_template('all_house_keepingtrans.html', items=items)

#++++UPDATE A Laundry TRANSACTION AS PAID++++
@app.route('/paid/<int:tran_id>')
def paid(tran_id):
    items = Cashitems.query.all()
    tran = Cashitems.query.get(tran_id)
    tran.paid = True
    db.session.commit()
    flash('Cash item paid', 'info')
    
    name = tran.customer_name + str(datetime.now().strftime("%H%M%S"))+'.pdf'
    with open(name, 'w+') as f:
            f.write(f'''
                    *********************************************************************
                    *********************************************************************
                                            RODICON GH
                                   Date: {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}  
                                       
                   Recieved from  {tran.customer_name}            Amount:GHc {tran.total}\n
                   An amount of {num2words(tran.total)} Ghana cedis                                  *
                   Being payment for  {num2words(tran.quantity)}({tran.quantity}) {tran.item_name}(s)                           
                  
                   Payment recieved by {current_user.username}                                                             
                    *********************************************************************
                    ''')
            iprint(name)
    return render_template('all_transactions.html', items=items)

#++++UPDATE A House Keeping TRANSACTION AS PAID++++
@app.route('/housekeepingpaid/<int:tran_id>')
def housekeepingpaid(tran_id):
    items = HouseCashitems.query.all()
    tran = HouseCashitems.query.get(tran_id)
    tran.paid = True
    db.session.commit()
    flash('Cash item paid', 'info')
    try:
            os.makedirs("C:/Users/Mashud/Desktop/Paid_receipts")
            os.chdir("C:/Users/Mashud/Desktop/Paid_receipts")
    except FileExistsError:
            os.chdir("C:/Users/Mashud/Desktop/Paid_receipts")    
    name = tran.customer_name + str(datetime.now().strftime("%H%M%S"))+'.pdf'
    with open(name, 'w+') as f:
            f.write(f'''
                    *********************************************************************
                    *********************************************************************
                                            RODICON GH
                                   Date: {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}  
                                       
                   Recieved from  {tran.customer_name}            Amount:GHc {tran.total}\n
                   An amount of {num2words(tran.total)} Ghana cedis                                  *
                   Being payment for  {num2words(tran.quantity)}({tran.quantity}) {tran.item_name}(s)                           
                  
                   Payment recieved by {current_user.username}                                                             
                    *********************************************************************
                    ''')
            iprint(name)
    return render_template('all_transactions.html', items=items)


@app.route('/receipts')
def receipts():
    return render_template('receipts.html')

#HOUSE KEEPING ROUTES
#1.HOUSE KEEPING EXPENSES ROUTE
@app.route('/house_keeping/expenses')
def house_keeping_expense():
    expenses =  Expense.query.filter_by(expense_type='H').all() 
    purchase =  Expense.query.with_entities(func.sum(Expense.amount)).filter_by(expense_type='H',category='Purchase' ).first(),
    salary = Expense.query.with_entities(func.sum(Expense.amount)).filter_by(expense_type='H',category='Salary' ).first()
    pur = purchase[0][0]
    sal = salary[0]
    
    values = [
                  pur, sal
                  
                   ] 
    return render_template('house_keeping_expenses.html', expenses=expenses, values=values)

#DELETE AN EXPENSES
@app.route('/expense/<expense_id>/delete')
def delete_expense(expense_id):
    expense=Expense.query.get(expense_id)
    db.session.delete(expense)
    db.session.commit()
    flash('Expense Deleted', 'success')
    return redirect(url_for('expenses'))

#DELETE A TRANSACTION
@app.route('/transaction/<transaction_id>/delete')
def delete_transaction(transaction_id):
    transact=Cashitems.query.get(transaction_id)
    db.session.delete(transact)
    db.session.commit()
    flash('Transaction Deleted', 'success')
    return redirect(url_for('transactions'))

#ALL ITEMS ADDED
@app.route('/items_and_prices')
def items_and_prices():
    items = Lundry_prices.query.all()
    return render_template('items_and_prices.html', items=items)

#DELETE AN ITEM
@app.route('/delete_item/<item_id>/delete')
def delete_item(item_id):
    item = Lundry_prices.query.get(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Item Deleted', 'success')
    return redirect(url_for('items_and_prices'))


#EDIT EXPENSE
@app.route('/edit_item/<item_id>/edit', methods=['GET','POST'])
def edit_item(item_id):
    form = AddLundryItem()
    if request.method == 'GET':
        item=Lundry_prices.query.get(item_id)
        form.item_name.data = item.item_name
        form.cost.data = item.price
        return render_template('edit_item_price.html', form=form, item=item)
    
    elif request.method == 'POST':
        if form.validate_on_submit():
            item= Lundry_prices.query.get(item_id)
            item.item_name = form.item_name.data
            item.price = form.cost.data
            db.session.commit()
            flash('Item Edit Successfully', 'Success')
            return redirect(url_for('items_and_prices'))
   

#DELETE A HOUSE KEEPING TRANSACTION
@app.route('/transact/<transaction_id>/delete')
def delete_house_keeping_transaction(transaction_id):
    transact=HouseCashitems.query.get(transaction_id)
    db.session.delete(transact)
    db.session.commit()
    flash('Transaction Deleted', 'success')
    return redirect(url_for('House_transactions'))


#DELETE A CUSTOMER
@app.route('/customer/<int:customer_id>/delete')
def delete_customer(customer_id):
    customer=Customers.query.get(customer_id)
    db.session.delete(customer)
    db.session.commit()
    flash('Customer Deleted', 'success')
    return redirect(url_for('about'))

#DELETE A COMPANY ASSET
@app.route('/asset/<int:asset_id>/delete')
def delete_asset(asset_id):
    myasset=Company_assets.query.get(asset_id)
    db.session.delete(myasset)
    db.session.commit()
    flash('Asset Deleted', 'success')
    return redirect(url_for('company_assets'))


#DELETE A CUSTOMER
@app.route('/employee/<int:employee_id>/delete')
def delete_employee(employee_id):
    employee= Employees.query.get(employee_id)
    db.session.delete(employee)
    db.session.commit()
    flash('Employee Deleted', 'success')
    return redirect(url_for('about'))
    
    

        
#EDIT EXPENSE
@app.route('/expense/<expense_id>/edit', methods=['GET','POST'])
def edit_expense(expense_id):
    form = AddExpenseForm()
    if request.method == 'GET':
        expense=Expense.query.get(expense_id)
        form.category.data = expense.category
        form.description.data = expense.description
        form.amount.data = expense.amount
        form.expense_category.data = expense.expense_type
        #sum of all purchases u
        purchase =  Expense.query.with_entities(func.sum(Expense.amount)).filter_by(category='Purchase' ).first(),
        #sum of all salaries
        salary = Expense.query.with_entities(func.sum(Expense.amount)).filter_by(category='Salary' ).first()
        pur = purchase[0][0]
        sal = salary[0]
        values = [pur, sal]
        return render_template('editexpense.html', form=form, expense=expense, values=values)
    
    elif request.method == 'POST':
        if form.validate_on_submit():
            expense=Expense.query.get(expense_id)
            expense.category = form.category.data
            expense.description = form.description.data
            expense.amount = form.amount.data
            db.session.commit()
            return redirect(url_for('about'))
    
#EDIT CUSTOMER INFO!!
@app.route('/customer/<int:customer_id>/edit', methods=['GET','POST'])
def edit_customer(customer_id):
    form = AddNewCustomer()
    if request.method == 'GET':
        
        customer=Customers.query.get(customer_id)
        form.customer_name.data = customer.customer_name
        form.location.data = customer.location
        form.service.data = customer.service
        form.gender.data = customer.gender
        form.phone.data = customer.phone
        values = [
                   Customers.query.filter_by(gender='M' ).count(),
                   Customers.query.filter_by(gender='F').count()
                   ] 
    
        return render_template('editcustomer.html', form=form, customer=customer, values=values)
    
    elif request.method == 'POST':
        if form.validate_on_submit():
            customer=Customers.query.get(customer_id)
            customer.customer_name = form.customer_name.data
            customer.location = form.location.data
            customer.phone = form.phone.data
            customer.service = form.service.data
            customer.gender = form.gender.data
            db.session.commit()
            return redirect(url_for('about'))
    
#EDIT EMPLOYEE DETAILS
@app.route('/emploee/<int:employee_id>/edit', methods=['GET','POST'])
def edit_employee(employee_id):
    form = AddEmployee()
    if request.method == 'GET':
        
        employee=Employees.query.get(employee_id)
        form.name.data = employee.name
        form.contact.data = employee.contact
        form.digital_address.data = employee.digital_address
        form.email.data = employee.email
        form.position.data = employee.position
        form.salary.data = employee.salary
        form.which_work.data = employee. employee_type
        form.gender.data = employee.gender
        
        values = [
            Employees.query.filter_by(gender='M', ).count(),
            Employees.query.filter_by(gender='F',).count()] 
        
        return render_template('editemployee.html', form=form, employee=employee, values=values)
    
    elif request.method == 'POST':
        if form.validate_on_submit():
            employee=Employees.query.get(employee_id)
            employee.name = form.name.data
            employee.contact = form.contact.data 
            employee.digital_address = form.digital_address.data
            employee.email= form.email.data
            employee.position = form.position.data
            employee.salary = form.salary.data 
            employee.employee_type = form.which_work.data 
            employee.gender = form.gender.data
              
            db.session.commit()
            flash('Edit was successful', 'success')
            #return redirect(url_for('about'))
            return redirect(url_for('myrec'))
        
@app.route('/myrec')
def myrec():
    return redirect('https://invoice-generator.com/#/1')        
 #EDIT AN ASSET 
@app.route('/asset/<int:asset_id>/edit', methods=['GET','POST'])
def edit_asset(asset_id):
    form = AddNewAsset()
    if request.method == 'GET':  
             
        comp_asset = Company_assets.query.get(asset_id)       
        form.name.data = comp_asset.name
        form.producers.data = comp_asset.producers
        form.code.data = comp_asset.code
        form.purchase_year.data = comp_asset.year_purchased
                
        return render_template('editasset.html', form=form, comp_asset=comp_asset)
    
    elif request.method == 'POST':
        if form.validate_on_submit():
            asset= Company_assets.query.get(asset_id)
            asset.name = form.name.data
            asset.producers = form.producers.data 
            asset.code = form.code.data
            asset.year_purchased= form.purchase_year.data
            db.session.commit()
            flash('Edit was successful', 'success')
            return redirect(url_for('company_assets'))
   

#2.HOUSE KEEPING ROUTE FOR CUSTOMERS
@app.route('/house_keeping/customers')
def house_keeping_customers():
    customers = Customers.query.filter_by(service = 'H').all()
    male_count = Customers.query.filter_by(gender='M', service='H').count()
    female_count =Customers.query.filter_by(gender='F', service='H').count()
    total  =  male_count + female_count
    if total > 0:
            
        male = round(male_count/ total * 100)
        female = round(female_count/total *100)
        return render_template('house_keeping_customers.html', customers=customers, male=male,female=female)      
    return render_template('house_keeping_customers.html', customers=customers)

#3.HOUSE KEEPINg EMPLOYEE PAGE ROUTE
@app.route('/house_keeping/employee')
def house_keeping_employee():
    from sqlalchemy import or_
    #if current_user.id ==1 or current_user.username == 'Admin':
        #return redirect(url_for('about'))
    employs = Employees.query.filter(or_(Employees.employee_type == 'H', Employees.employee_type=='B')).all() 
    values = [
    Employees.query.filter(or_(Employees.employee_type == 'H', Employees.employee_type=='B'),Employees.gender=='M').count(),
    Employees.query.filter(or_(Employees.employee_type == 'H', Employees.employee_type=='B'),Employees.gender=='F').count()] 
      
    return render_template('house_keeping_employee.html', employs=employs, values=values)


@app.route('/house_keeping/summary')
def house_keeping_summary():
    cash =  HouseCashitems.query.with_entities(func.sum(Cashitems.total)).filter_by(paid=1).all(),
    mycash = cash[0][0][0]
    values = {}
    import calendar
    from sqlalchemy import or_
    for i in range(1,13):
        
        monthly_customers = Customers.query.filter(
                    extract('month', Customers.date_created) == i,
                    Customers.service == 'H').count()
            
        monthly_cash = HouseCashitems.query.with_entities(func.sum(Expense.amount)).filter(
                    extract('month', Customers.date_created) == i,
                    Cashitems.paid == 1).all()
            
        monthly_expense = Expense.query.with_entities(func.sum(Expense.amount)).filter(
                    extract('month', Customers.date_created) == i,
                    Expense.expense_type == 'H').all()
            
        if i == datetime.today().month + 1:
                break
        i = calendar.month_name[i]        
        values.update({i:[monthly_customers, monthly_cash[0][0], monthly_expense[0][0]]})    
    print(values)         
            
    if mycash is None:
        mycash = 0
    custom = Customers.query.filter_by(service = 'H').count()
    empl = Employees.query.filter(or_(Employees.employee_type == 'H', Employees.employee_type=='B')).count()
    expense = Expense.query.with_entities(func.sum(Expense.amount)).filter_by(expense_type='H').all()
    myexpense = expense[0][0]
    if myexpense is None:
        myexpense = 0
    
    if mycash > 0 and myexpense > 0:    
        total_cash= mycash + myexpense 
        mycash_percent = round(mycash/total_cash * 100) 
        myexpense_percent = round(myexpense/total_cash * 100)
    else:
        mycash_percent  = 0  
        myexpense_percent= 0     
    return render_template('house_keeping_summary.html',values= values,mycash_percent=mycash_percent,myexpense_percent=myexpense_percent, empl=empl,mycash=mycash,custom=custom,myexpense=myexpense)

@app.route('/setting', methods=['GET','POST'])
def setting():
    
    form = AddLundryItem()
    form2 = AddEmployeePayroll()
    form3 = DeductAllPayroll()
    form4 = DeductFromAnEmployee()
    db.create_all()
    form = AddLundryItem()
    form = AddLundryItem()
    if form.validate_on_submit():
        item = Lundry_prices(
                item_name = form.item_name.data,
                price = form.cost.data
            )
        db.session.add(item)
        db.session.commit()
        flash('New item added successfully', 'success')
    return render_template('setting.html', form=form, form2=form2,form3=form3,form4=form4)
    
    


#***FUNCTION TO SEND EMAIL
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
                  sender='smasahudu97@gmail.com',
                   recipients=[user.email])
    
    msg.body = f''' 
    To reset your password, visit the following link:
    {url_for('reset_token', token=token, _external =True)}
    
    if you did not send this request, simply ignore this message and no changes will be made
    '''
    mail.send(msg)

#REQUEST PAGE FOR A NEW PASSWORD
@app.route('/reset_password', methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('about'))
    form = RequestResetForm()
    user = User.query.filter_by(email = form.email.data).first()
    
   
    if form.validate_on_submit():
            if user is None:
                flash('Email does not exist, Recheck your email.', 'danger')
                return redirect(url_for('reset_request')) 
            send_reset_email(user)
            flash('An Email has been sent with instructions to reset your password', 'info')
            return redirect(url_for('login'))     
    return render_template('reset_request.html', form=form)

#PASSWORD SENT NOW ENTER NEW PASSWORD TO RESET
@app.route('/reset_password/<token>', methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('about'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            flash(f'Your password has been updated, You can please Log in', 'success')
            return redirect(url_for('login'))
      
    return render_template('reset_token.html', form=form)
    

if __name__ == '__main__':
    app.run(debug=True)