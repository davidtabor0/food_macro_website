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