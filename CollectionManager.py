from pymongo import MongoClient
from dotenv import load_dotenv
import os

class CollectionManager:
    """
    Object to manage collections with MongoDB.
    """
    def __init__(self, db_name: str, collection_name: str):
        """
        Initialize the CollectionManager object.
        """
        self.db_name = db_name
        self.collection_name = collection_name
        self.connection_string = self.load_connection_string()
        self.client = None  # Set by connect()
        self.db = None  # Set by connect()
        self.collection = None  # Set by connect() 
        self.connect()

    def load_connection_string(self) -> str:
        """
        Load the connection string from the .env file.
        """
        load_dotenv()
        return os.getenv('CONN_STR')

    def connect(self):
        """
        Connect to MongoDB and set up collection.
        """
        if not self.client:
            self.client = MongoClient(self.connection_string)
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]

    def insert_one_doc(self, document: dict):
        """
        Inserts a document into the collection.
        
        document: MongoDB document.
        """
        self.collection.insert_one(document)

    def find_one_doc(self, query: dict, projection: dict = None) -> dict:
        """
        Finds a document within the collection.

        query: Filter to find your document.
        projection: Optional filter to only return certain fields of a document.
        """
        return self.collection.find_one(query, projection)
    
    def find_many_docs(self, query: dict = {}, projection: dict = None):
        """
        Finds multiple matching documents within the collection.

        query: Filter to find your documents.
        projection: Optional filter to only return certain fields of a document.
        returns: iterable pymongo cursor object. 
        """
        return self.collection.find(query, projection)
    
    def delete_many_docs(self, filter : dict):
        """
        Deletes multiple matching documents within the collection.

        filter: Filter to find your documents.
        """
        return self.collection.delete_many(filter)
    
    def update_one_doc(self, filter : dict, update : dict):
        """
        Updates one document in the collection based on the filter and new data in update.

        filter: Filter to find your document to update.
        update: New data to be updated. 
        """
        return self.collection.update_one(filter, update)
    
    def update_many_docs(self, filter : dict):
        """
        Updates all documents matching the filter.

        filter: Filter to find your documents.
        update: New data to be updated.
        """
        return self.collection.delete_many(filter)
    
    def count_docs(self, filter : dict = {}) -> int:
        """
        Counts number of documents in the collection and returns that value.

        filter: Filter to find your documents.
        returns: integer
        """
        return self.collection.count_documents(filter)
    
