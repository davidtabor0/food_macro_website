from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# routes bind to the function below its definition.
@app.route('/')
@app.route('/home')
def hello():
    return render_template('home.html')

@app.route('/dog')
def dog():
    carbs = 100
    fats = 150
    proteins = 200
    return render_template('tracking.html', carbs=carbs, fats=fats, proteins=proteins)

@app.route('/submit-fat', methods=['POST'])
def submit_fat():
    fat = int(request.form['fatInput'])
    print("Fat eaten:", fat)
    return redirect(url_for('dog'))
    
@app.route('/submit-carbs', methods=['POST'])
def submit_carbs():
    carbs = int(request.form['carbsInput'])
    print("Carbs eaten:", carbs)
    return redirect(url_for('dog'))

@app.route('/submit-protein', methods=['POST'])
def submit_protein():
    protein = int(request.form['proteinInput'])
    print("Carbs eaten:", protein)
    return redirect(url_for('dog'))

# If this file is run to launch the flask server, instead of using commands, then the server launches in debug.
if __name__ == '__main__':
    app.run(debug=True)