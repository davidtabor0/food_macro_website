from flask import Flask
from routes import bp
from CollectionManager import CollectionManager

app = Flask(__name__)

my_collection = CollectionManager('MacroTracker', 'testing123')

# Placeholder values if the collection has no values yet.
doc_count = my_collection.count_docs()
if doc_count == 0:
    empty_macros = {
        'fat' : 0,
        'carbs' : 0,
        'protein': 0,
    }
    my_collection.insert_one_doc(empty_macros)

# Register the blueprint created in routes.py
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)  # Run in debug mode.