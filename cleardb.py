from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
client =  MongoClient(os.getenv('CONN_STR'))
db = client['MacroTracker']
user_collection = db['Users']
data_collection = db['Data']
inp = input('\nAre you sure you would like to completely wipe both collections? (y to confirm): ')
if inp == 'y' or inp == 'Y':
    result_user = user_collection.delete_many({})
    result_data = data_collection.delete_many({})
    print(f'\nDeleted {result_user.deleted_count} documents from User collection.')
    print(f'Deleted {result_data.deleted_count} documents from Data collection.\n')
else:
    print('Process aborted.')