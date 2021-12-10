from bson.json_util import dumps
from pymongo import MongoClient
import sys


def export_collection(db_name, collection_name, export_file):
    mongo_client = MongoClient("mongodb://127.0.0.1:27017")
    gamedb = mongo_client[db_name]
    games_col = gamedb[collection_name]

    try:
        doc_count = games_col.count_documents({})
        cursor = games_col.find({})
        with open(export_file, 'w') as file:
            file.write('[')
            for i, document in enumerate(cursor, 1):
                file.write(dumps(document))
                if i != doc_count:
                    file.write(',')            
            file.write(']')

        print('finish export!')
        mongo_client.close()
    except Exception as e:
        print(e)
        mongo_client.close()



def main():
    export_collection('gamedb', 'publishers', 'publishers.json')
    pass

if __name__ == '__main__':
    main()