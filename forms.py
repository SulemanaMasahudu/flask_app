import flask_wtf
from flask_wtf import FlaskForm
from  wtforms import StringField,IntegerField, HiddenField,PasswordField, SubmitField, BooleanField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max = 20)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])


    submit = SubmitField('Sign Up')
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max = 220)])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

    remember_me = BooleanField('Remember me',)

    submit = SubmitField('Login')
    
 #add cash  for laundry services 
class AddCashForm(FlaskForm):
    
    customer_name = StringField('Customer name', validators=[DataRequired(), Length(max = 250)])

    itemname = StringField('Item name', validators=[DataRequired(), Length(max = 250)])
    
    price = IntegerField('Price', validators=[DataRequired(),])
    
    quantity = SelectField('Quantity', 
                           choices = [('1', '1'),
                                      ('2', '2'),
                                      ('3', '3'),
                                      ('4', '4'),
                                      ('5', '5'),
                                      ('6', '6'),
                                      ('7', '7'),
                                      ('8', '8'),
                                      ('9', '9'),
                                      ('10', '10'),
                                      ('11', '11'),
                                      ('12', '12'),
                                      ('13', '13'),
                                      ('14', '14'),
                                      ('15', '15'),
                                      ('16', '16'),
                                      ('17', '17'),
                                      ('18', '18'),
                                      ('19', '19'),
                                      ('20', '20')],validators=[DataRequired(), Length(max = 20)])
    
    total = StringField('Total', validators=[DataRequired(), Length(max = 20)])
    
    submit = SubmitField('Submit')


 #add cash  for laundry services 
class AddHouseCashForm(FlaskForm):
    
    customer_name = StringField('Customer name', validators=[DataRequired(), Length(max = 250)])

    itemname = StringField('Item name', validators=[DataRequired(), Length(max = 250)])
    
    price = IntegerField('Price', validators=[DataRequired(),])
    
    quantity = SelectField('Quantity', 
                           choices = [('1', '1'),
                                      ('2', '2'),
                                      ('3', '3'),
                                      ('4', '4'),
                                      ('5', '5'),
                                      ('6', '6'),
                                      ('7', '7'),
                                      ('8', '8'),
                                      ('9', '9'),
                                      ('10', '10'),
                                      ('11', '11'),
                                      ('12', '12'),
                                      ('13', '13'),
                                      ('14', '14'),
                                      ('15', '15'),
                                      ('16', '16'),
                                      ('17', '17'),
                                      ('18', '18'),
                                      ('19', '19'),
                                      ('20', '20')],validators=[DataRequired(), Length(max = 20)])
    
    total = StringField('Total', validators=[DataRequired(), Length(max = 20)])
    
    submit = SubmitField('Submit')
        
#Add expense for laundry businesss    
class AddExpenseForm(FlaskForm):
    
    category = SelectField('Category', validators=[DataRequired()],
                           choices=[('Purchase','Purchases'),
                                    ('Salary','Salaries')])

    description = StringField('Description', validators=[DataRequired(), Length( max = 250)])
    
    amount = IntegerField('Amount', validators=[DataRequired(),])
    
    expense_category = RadioField('Expense Category', choices = [('L','Laundry Service'),('H','House Keeping')])

    submit = SubmitField('Submit')    

#Add a new customer for laundry business
class AddNewCustomer(FlaskForm):
    
    customer_name = StringField('Customer Name', validators=[DataRequired(), Length(max = 250)])

    location = StringField('Location', validators=[DataRequired(), Length( max = 250)])
    
    gender = RadioField('Gender', choices = [('M','Male'),('F','Female')])
    service = RadioField('Service', choices = [('L','Laundry'),('H','House keeping')])
    
    phone= IntegerField('Phone', validators=[DataRequired(),])
    
    submit = SubmitField('Submit')
        


#Add a new company asset
class AddNewAsset(FlaskForm):
    
    name = StringField('Name of Asset', validators=[DataRequired(), Length(max = 100)])

    producers = StringField('Producers', validators=[DataRequired(), Length( max = 50)])
    
    code= StringField('Code', validators=[DataRequired(), Length(max = 20)])
    
    purchase_year= StringField('Year Of Purcharse', validators=[DataRequired(), Length(max = 20)])
    
    submit = SubmitField('Submit')
        

#Add a new Employee
class AddEmployee(FlaskForm):
    
    name = StringField('Name', validators=[DataRequired(), Length(max = 100)])

    contact = IntegerField('Contact', validators=[DataRequired(),])
    
    digital_address= StringField('Digital Address', validators=[DataRequired(), Length(max = 100)])
    
    email= StringField('Email', validators=[DataRequired(), Email()])
    
    position= StringField('Position', validators=[DataRequired(),])
    
    salary= IntegerField('Salary', validators=[DataRequired(),])
    
    which_work = RadioField('Work Category', choices = [('L','Laundry Service'),('H','House Keeping'),('B','Both')])
    
    gender = RadioField('Gender', choices = [('F','Female'),('M','Male')])
    
    submit = SubmitField('Submit')
    
#ADD EMPLOYEE PAYROLL

class AddEmployeePayroll(FlaskForm):
    
    name = StringField('Name', validators=[DataRequired(), Length(max = 200)])
    
    user_id = StringField(validators=[DataRequired(),Length(max = 200)])
    
    position= StringField('Position', validators=[DataRequired(),])
    
    salary= StringField('Salary', validators=[DataRequired()])
    
    which_work = SelectField('Work Category', 
                           choices = [('S', 'Select Category'),
                                      ('L', 'Laundry'),
                                      ('H', 'House Keeping'),
                                      ('B', 'Both'),
                                      
                                      ],validators=[DataRequired(),Length(max = 20)])
       
    
    submit_pay = SubmitField('Submit Pay')
    
class DeductAllPayroll(FlaskForm):
    
    about_deduction = StringField('About', validators=[DataRequired(),])
    
    amount_deducted = IntegerField('Amount', validators=[DataRequired(),])
       
    submit_deduct = SubmitField('Deduct')
    

class DeductFromAnEmployee(FlaskForm):
    
    name = StringField('Name', validators=[DataRequired(), Length(max = 200)])
    
    user_id = StringField(validators=[DataRequired(),Length(max = 200)])
    
    position= StringField('Position', validators=[DataRequired(),])
    
    amount_deducted= StringField('Amount Deducted', validators=[DataRequired()])
    
    about_deduction = StringField('About Deduction', validators=[DataRequired(),])
    
    which_work = SelectField('Work Category', 
                           choices = [('S', 'Select Category'),
                                      ('L', 'Laundry'),
                                      ('H', 'House Keeping'),
                                      ('B', 'Both'),
                                      
                                      ],validators=[DataRequired(),Length(max = 20)])
       
    
    deduct = SubmitField('Deduct')
  

class AddLundryItem(FlaskForm):
    
    item_name = StringField('Lundry Item', validators=[DataRequired(), Length(max = 100)])
    
    cost= IntegerField('Price', validators=[DataRequired(),])
    
    submit = SubmitField('Submit')
    
    
class AddHouseItem(FlaskForm):
    
    house_type = StringField('Name', validators=[DataRequired(), Length(max = 100)])
    
    cost= IntegerField('Salary', validators=[DataRequired(),])
    
    submit = SubmitField('Submit')
    
    
    
class RequestResetForm(FlaskForm):
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Reset Password')
    
   

    
    
            
    