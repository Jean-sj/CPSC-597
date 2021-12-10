import sys
import os
import codecs
import json
from elasticsearch import Elasticsearch, helpers

es = Elasticsearch()

def import_json(json_file, index_name, type_name):
    source_list = []
    with open(json_file, 'r+') as fhandler:
        source_list = json.load(fhandler)

    id_num = 1
    actions = []
    
    for source in source_list:
        del source['_id']
        action = {
            '_index': index_name,
            '_type': type_name,
            '_id': id_num
        }
        action.update(source)
        id_num += 1
        actions.append(action)
        if (len(actions) == 500):
            helpers.bulk(es, actions)
            del actions[0:len(actions)]
    if (len(actions) > 0):  
        helpers.bulk(es, actions) 

def import_json_with_pic_path(json_file, index_name, type_name):
    
    source_list = []
    with open(json_file, 'r+') as fhandler:
        source_list = json.load(fhandler)

    id_num = 1
    actions = []

    for source in source_list:
        del source['_id']
        action = {
            '_index': index_name,
            '_type': type_name,
            '_id': id_num
        }
        source['pic'] = get_match_pic_file(source['name'])        
        action.update(source)
        id_num += 1
        actions.append(action)
        if (len(actions) == 500):
            helpers.bulk(es, actions)
            del actions[0:len(actions)]
    if (len(actions) > 0):  
        helpers.bulk(es, actions) 
    

def get_match_pic_file(game_name):
    body = {
        "query": {
            "bool": {
                "must": []
            }
        }
    }

    body["query"]["bool"]["must"].append({
        "match": {"name": game_name}
    })

    res = es.search(
        index="gamepics",
        body=body
    )

    pic_name = ""
    if len(res['hits']['hits']) > 0:
        game_source = res['hits']['hits'][0]['_source']
        console = game_source['console']
        pic_name = console + "/" + game_source['name']

    return pic_name

    # pics_dict = {}
    # for i in res['hits']['hits']:
    #     game_source = res['hits']['hits']['_source']
    #     console = game_source['console']
    #     if not console in pics_dict:
    #         pics_dict[console] = game_source['name'] 

    # return pics_dict


def main():
    # import_json('games.json', 'games', 'game')
    import_json_with_pic_path('games.json', 'games', 'game')
    print('finished!')

if __name__ == "__main__":
    main()