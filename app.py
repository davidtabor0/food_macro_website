from flask import Flask, render_template

app = Flask(__name__)

# routes bind to the function below its definition.
@app.route('/')
@app.route('/home')
def hello():
    return render_template('home.html')

@app.route('/dog')
def dog():
    return render_template('tracking.html')

# If run this file instead of using commands, then server launches in debug.
if __name__ == '__main__':
    app.run(debug=True)