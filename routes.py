from flask import Blueprint, render_template, request, redirect, url_for

#Initialize blueprint
bp = Blueprint('routes', __name__)

#Define routes to the blueprint
@bp.route('/home')
def hello():
    return render_template('home.html')

@bp.route('/')
@bp.route('/tracking') 
def tracking():
    global carbs, fat, protein
    return render_template('tracking.html', carbs=carbs, fat=fat, protein=protein)

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