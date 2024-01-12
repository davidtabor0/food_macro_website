from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from pymongo import MongoClient
import os
from datetime import datetime

# Initialize a collections
load_dotenv()
client =  MongoClient(os.getenv('CONN_STR'))
db = client['MacroTracker']
user_collection = db['Users']
data_collection = db['Data']

# Create login and submit form classes.
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class IntegerForm(FlaskForm):
    number = IntegerField()
    submit = SubmitField('Submit')


#Initialize blueprint to save the routes to.
bp = Blueprint('routes', __name__)

#Define routes to the blueprint
# HOME
@bp.route('/home')
def hello():
    return render_template('home.html')

# TRACKING
@bp.route('/')
@bp.route('/tracking')  # Should only be accessible to logged in users. TODO
def tracking():
    global data_collection
    fatform = IntegerForm()
    carbform = IntegerForm()
    proteinform = IntegerForm()
    #date = datetime.now().isoformat()[:10]
    user_id = session.get('user_id')
    # Retrieve the most recent document from the current user
    saved_values = data_collection.find_one({'user_id': user_id})
    return render_template('tracking.html', saved_values=saved_values, carbform=carbform, proteinform=proteinform, fatform=fatform)

# LOGIN
@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # Data processing when submitted.
        global user_collection

        email = form.email.data
        password = form.password.data

        # Get user by matching email from DB.
        user = user_collection.find_one({'email': email})
        if user:  #Check if user exists.
            passsword_hash = user['password']
            if check_password_hash(passsword_hash, password):
                session['user_id'] = str(user['_id'])  # Set user_id for the session as the _id of their entry in Mongo.
                
                # TODO Flash a message confirming their login before redirecting.
                print('Login Success.')

                return redirect('/tracking')
            else:  #If passwords dont match.
                return redirect('/login')
        else:  #If user doesn't exist.
            return redirect('/login')

    return render_template('login.html', form=form)

# REGISTER
@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():  # Submission logic
        global user_collection
        global data_collection

        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        
        # Check if email address is valid.
        if not '@' in email:
            print('Invalid email address.')
            # TODO flash message about registration failure.

        # Check if email is already registered
        user = user_collection.find_one({'email': email})
        if user:
            print('Email already exists.')
            # TODO flash message about registration failure
            return redirect('/register')
        
        # Check if passwords match
        if password != confirm_password:
            print('Passwords do not match.')
            # TODO flash message about registration failure
            return redirect('/register')
        
        # All checks passed, hash password and save new user to DB.
        password_hash = generate_password_hash(password)
        new_user = {
            'email': email, 
            'password': password_hash
        }
        user_collection.insert_one(new_user)
        print('Registration success.')
        # TODO flash message about registration success.

        # Insert day one log into the data collection for this user.
        user = user_collection.find_one({'email': email})
        date = datetime.now().isoformat()[:10]
        new_data = {
            'user_id' : str(user['_id']),
            'date' : date,
            'fat' : 0,
            'carbs' : 0,
            'protein': 0,
            }
        data_collection.insert_one(new_data)
        return redirect('/login')
    return render_template('register.html', form=form) 

# SUBMIT FAT
@bp.route('/submitfat', methods=['POST'])
def submitfat():
    global data_collection
    user_id = session.get('user_id')
    document = data_collection.find_one({'user_id' : user_id})
    current_fat = document['fat']
    form = IntegerForm()
    if form.validate_on_submit():  # Data processing when submitted.
        new_fat = form.number.data
        updated_fat = current_fat + new_fat
        data_collection.update_one(document, {'$set': {'fat': updated_fat}})
        return redirect(url_for('routes.tracking'))
    return redirect(url_for('routes.tracking')) 

# SUBMIT CARBS
@bp.route('/submit-carbs', methods=['POST'])
def submit_carbs():
    global data_collection
    document = data_collection.find_one({})
    current_carbs = document['carbs']
    form = IntegerForm()
    if form.validate_on_submit():  # Data processing when submitted.
        new_carbs = form.number.data
        updated_carbs = current_carbs + new_carbs
        data_collection.update_one(document, {'$set': {'carbs': updated_carbs}})
        return redirect(url_for('routes.tracking'))
    return redirect(url_for('routes.tracking'))

# SUBMIT PROTEIN
@bp.route('/submit-protein', methods=['POST'])
def submit_protein():
    global data_collection
    document = data_collection.find_one({})
    current_protein = document['protein']
    form = IntegerForm()
    if form.validate_on_submit():  # Data processing when submitted.
        new_protein = form.number.data
        updated_protein = current_protein + new_protein
        data_collection.update_one(document, {'$set': {'protein': updated_protein}})
        return redirect(url_for('routes.tracking'))
    return redirect(url_for('routes.tracking')) 
