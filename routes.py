from flask import Blueprint, render_template, request, redirect, url_for
from CollectionManager import CollectionManager
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
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
@bp.route('/tracking') 
def tracking():
    global my_collection
    fatform = IntegerForm()
    carbform = IntegerForm()
    proteinform = IntegerForm()
    saved_values = my_collection.find_one_doc({})
    return render_template('tracking.html', saved_values=saved_values, carbform=carbform, proteinform=proteinform, fatform=fatform)

# LOGIN
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

# REGISTER
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

# SUBMIT FAT
@bp.route('/submitfat', methods=['POST'])
def submitfat():
    global my_collection
    document = my_collection.find_one_doc({})
    current_fat = document['fat']
    form = IntegerForm()
    if form.validate_on_submit():  # Data processing when submitted.
        new_fat = form.number.data
        updated_fat = current_fat + new_fat
        my_collection.update_one_doc(document, {'$set': {'fat': updated_fat}})
        return redirect(url_for('routes.tracking'))
    return redirect(url_for('routes.tracking')) 

# SUBMIT CARBS
@bp.route('/submit-carbs', methods=['POST'])
def submit_carbs():
    global my_collection
    document = my_collection.find_one_doc({})
    current_carbs = document['carbs']
    form = IntegerForm()
    if form.validate_on_submit():  # Data processing when submitted.
        new_carbs = form.number.data
        updated_carbs = current_carbs + new_carbs
        my_collection.update_one_doc(document, {'$set': {'carbs': updated_carbs}})
        return redirect(url_for('routes.tracking'))
    return redirect(url_for('routes.tracking'))

# SUBMIT PROTEIN
@bp.route('/submit-protein', methods=['POST'])
def submit_protein():
    global my_collection
    document = my_collection.find_one_doc({})
    current_protein = document['protein']
    form = IntegerForm()
    if form.validate_on_submit():  # Data processing when submitted.
        new_protein = form.number.data
        updated_protein = current_protein + new_protein
        my_collection.update_one_doc(document, {'$set': {'protein': updated_protein}})
        return redirect(url_for('routes.tracking'))
    return redirect(url_for('routes.tracking')) 
