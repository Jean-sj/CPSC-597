import sys
import os
import re
import uuid
import codecs
import json
from elasticsearch import Elasticsearch, helpers

def import_image(pic_path, console_type):
    es = Elasticsearch()
    id_num = 1
    actions = []

    source_list = []

    pic_list = os.listdir(pic_path)
    for pic_name in pic_list:        
        source = { "name": pic_name, "console": console_type }
        source_list.append(source)
    

    id_num = 1
    actions = []

    for source in source_list:
        action = {
            '_index': "gamepics",
            '_type': "gamepic",
            '_id': str(uuid.uuid4())
        }
        action.update(source)
        id_num += 1
        actions.append(action)
        if (len(actions) == 500):
            helpers.bulk(es, actions)
            del actions[0:len(actions)]
    if (len(actions) > 0):  
        helpers.bulk(es, actions)

def rename_file(pic_path):
    pic_list = os.listdir(pic_path)
    for pic_name in pic_list:
        old_pic_name = pic_name                
        new_pic_name = re.sub('[#\[\]]', "", pic_name)
        os.rename(pic_path + "\\" + old_pic_name, pic_path + "\\" + new_pic_name)
    

def main():
    import_image('images\\switch', 'nintendo switch')
    # rename_file('images\\xbox')
    print('finished!')

if __name__ == "__main__":
    main()