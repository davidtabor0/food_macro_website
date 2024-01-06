from flask import Blueprint, render_template, request, redirect, url_for
from CollectionManager import CollectionManager

# Initialize a collection under DB name 'MacroTracker' and collection name 'testing123'
my_collection = CollectionManager('MacroTracker', 'testing123')

#Initialize blueprint
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

@bp.route('/submit-fat', methods=['POST'])
def submit_fat():
    global fat
    new_fat = int(request.form['fatInput'])
    fat += new_fat
    return redirect(url_for('tracking'))
    
@bp.route('/submit-carbs', methods=['POST'])
def submit_carbs():
    global carbs
    new_carbs = int(request.form['carbsInput'])
    carbs += new_carbs
    return redirect(url_for('tracking')) # <- item in quotes is the name of the function for that route.

@bp.route('/submit-protein', methods=['POST'])
def submit_protein():
    global protein
    new_protein = int(request.form['proteinInput'])
    protein += new_protein
    return redirect(url_for('tracking'))