from flask import Blueprint, render_template, request, redirect, url_for
from CollectionManager import CollectionManager
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

# Initialize a collection under DB name 'MacroTracker' and collection name 'testing123'
my_collection = CollectionManager('MacroTracker', 'testing123')

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

#Initialize blueprint to save the routes to.
bp = Blueprint('routes', __name__)

#Define routes to the blueprint
@bp.route('/home')
def hello():
    return render_template('home.html')

@bp.route('/')
@bp.route('/tracking') 
def tracking():
    global my_collection
    document = my_collection.find_one_doc({})
    fat, carbs, protein = document['fat'], document['carbs'], document['protein']
    return render_template('tracking.html', fat=fat, carbs=carbs, protein=protein)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # Data processing when submitted.
        email = form.email.data
        password = form.password.data
        print(f'\n\n!User Login!\nEmail: {email}\nPassword: {password}\n\n')
        #TODO Find matching user if exists in DB and log thm in.
        return redirect('/tracking')  # Send the user to the main page of interest after they log in.
    return render_template('login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():  # Submission logic
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        #Check if data is valid
        #i.e., valid email, appropriate password, matching passwords, user doesnt exist already, etc.
        return redirect('/login')
    return render_template('register.html', form=form) 

@bp.route('/submit-fat', methods=['POST'])
def submit_fat():
    global my_collection
    document = my_collection.find_one_doc({})
    fat = document['fat']
    new_fat = int(request.form['fatInput'])
    updated_fat = fat + new_fat
    my_collection.update_one_doc(document, {'$set': {'fat': updated_fat}})
    return redirect(url_for('routes.tracking')) # <- item in quotes is the name of the function for that route.

@bp.route('/submit-carbs', methods=['POST'])
def submit_carbs():
    global my_collection
    document = my_collection.find_one_doc({})
    carbs = document['carbs']
    new_carbs = int(request.form['carbsInput'])
    updated_carbs = carbs + new_carbs
    my_collection.update_one_doc(document, {'$set': {'carbs': updated_carbs}})
    return redirect(url_for('routes.tracking')) # <- item in quotes is the name of the function for that route.

@bp.route('/submit-protein', methods=['POST'])
def submit_protein():
    global my_collection
    document = my_collection.find_one_doc({})
    protein = document['protein']
    new_protein = int(request.form['proteinInput'])
    updated_protein = protein + new_protein
    my_collection.update_one_doc(document, {'$set': {'protein': updated_protein}})
    return redirect(url_for('routes.tracking'))