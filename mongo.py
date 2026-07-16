import sys
import json
from pymongo import MongoClient
from tabulate import tabulate

mongo_uri = "mongodb://PGSAppUser:V7mQ2xLp9Nz4Kc81@pgs-dub-prd-mdb-01.paysecure.internal:27017,pgs-dub-prd-mdb-02.paysecure.internal:27017,pgs-dub-prd-mdb-03.paysecure.internal:27017/pgsproddb?authSource=admin&replicaSet=replSETiR&readPreference=secondaryPreferred"
# mongo_uri = "mongodb://localhost:27017/kg"

def main():
    action = sys.argv[1] if len(sys.argv) > 1 else None
    
    client = MongoClient(mongo_uri)
    
    try:
        db = client.get_database()
        
        if action == 'tables':
            collections = db.list_collection_names()
            
            table_data = [[name] for name in collections]
            print(tabulate(table_data, headers=['name'], tablefmt='grid'))
        
        elif action == 'count':
            table = sys.argv[2] if len(sys.argv) > 2 else None
            if not table:
                print("Error: table name required")
                return
            
            count = db[table].count_documents({})
            print(count)
        
        elif action == 'sample':
            table = sys.argv[2] if len(sys.argv) > 2 else None
            limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
            
            if not table:
                print("Error: table name required")
                return
            
            docs = db[table].find({}).sort('_id', -1).limit(limit)
            
            docs_list = list(docs)
            print(json.dumps(docs_list, indent=2, default=str))
        
        elif action == 'dump':
            table = sys.argv[2] if len(sys.argv) > 2 else None
            if not table:
                print("Error: table name required")
                return
            
            docs = db[table].find({}).to_list(length=None)
            
            with open(f'{table}.json', 'w') as f:
                json.dump(docs, f, indent=2, default=str)
            
            print(f'{table}.json created ({len(docs)} docs)')
        
        else:
            print("""
Usage:

python mongo.py tables

python mongo.py count users

python mongo.py sample users

python mongo.py sample users 50

python mongo.py dump users
""")
    
    finally:
        client.close()

if __name__ == '__main__':
    main()
