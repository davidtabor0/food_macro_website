from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

carbs = 0
fat = 0
protein = 0

# routes bind to the function below its definition.
@app.route('/home')
def hello():
    return render_template('home.html')

@app.route('/')
@app.route('/tracking') 
def tracking():
    global carbs, fat, protein
    return render_template('tracking.html', carbs=carbs, fat=fat, protein=protein)

@app.route('/submit-fat', methods=['POST'])
def submit_fat():
    fat = int(request.form['fatInput'])
    print("Fat eaten:", fat) # TESTING
    return redirect(url_for('tracking'))
    
@app.route('/submit-carbs', methods=['POST'])
def submit_carbs():
    global carbs
    new_carbs = int(request.form['carbsInput'])
    print("before", carbs)
    carbs += new_carbs
    print("Carbs eaten:", new_carbs) # TESTING
    print("after", carbs)
    return redirect(url_for('tracking')) # <- item in quotes is the name of the function for that route.

@app.route('/submit-protein', methods=['POST'])
def submit_protein():
    protein = int(request.form['proteinInput'])
    print("Carbs eaten:", protein) # TESTING
    return redirect(url_for('tracking'))

# If this file is run to launch the flask server, instead of using commands, then the server launches in debug.
if __name__ == '__main__':
    app.run(debug=True)