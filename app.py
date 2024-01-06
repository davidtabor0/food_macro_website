from flask import Flask
from routes import bp
from CollectionManager import CollectionManager

app = Flask(__name__)

# Register the blueprint created in routes.py
app.register_blueprint(bp)

my_collection = CollectionManager('MacroTracker', 'testing123') 
docu = {'xD' : '123'}
my_collection.insert_one_doc(docu)

if __name__ == '__main__':
    app.run(debug=True)  # Run in debug mode.