import atexit
from flask import Flask, render_template, request, jsonify
from elasticsearch import Elasticsearch
import json
import sys
import string
from neo4j import GraphDatabase

app = Flask(__name__)
driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'neo4j'))
es = Elasticsearch()


@app.route('/')
def index():
    return render_template("search.html", title="Game Knowledge Graph Search")

@app.route('/querygames', methods=['GET', 'POST'])
def query():
    params = request.get_json()
    body = {
        "from": params["from"],
        "size": params["size"],
        "query": {
            "bool": {
                "must": [],
                "must_not": []
            }
        }
    }
    body["query"]["bool"]["must_not"].append({
        "term": {"pic.keyword": ""}
    })
    
    search_type = params["type"].lower()
    if params['name'] != '':
        if search_type == "developer":
            body["query"]["bool"]["must"].append({
                "match": {"developers": params["name"]}
            })
        elif search_type == "publisher":
            body["query"]["bool"]["must"].append({
                "match": {"publishers": params["name"]}
            })
        else:
            body["query"]["bool"]["must"].append({
                "match": {"name": params["name"]}
            })

    if params["genres"] != 'All':
        body["query"]["bool"]["must"].append({
            "match": {"source.genres": params["genres"]}
        })
    # if params["releaseyear"] != 'All':
    #     body["query"]["bool"]["must"].append({
    #         "match": {"source.release_date": params["releaseyear"]}
    #     })
    if params['platform'] != 'All':
        body["query"]["bool"]["must"].append({
            "match": {"platform": params["platform"]}
        })    

    res = es.search(
        index="games", 
        body=body)

    return jsonify(res)

@app.route('/details/<id>')
def details(id):
    body = {
        "query": {
            "match": {
                "_id": id
            }
        }
    }

    res = es.search(
        index="games", 
        body=body)
    
    game_info_dict = None
    rel_game_list = []
    if len(res['hits']['hits']) > 0:
        game_info_dict = res['hits']['hits'][0]['_source']
        with driver.session() as session:
            cql = 'MATCH (g1:Game {name: "' + game_info_dict['name'] + '"})-[*..2]-(g2:Game) RETURN g2 LIMIT 12'
            results = session.run(cql).values()
            for result in results:
                rel_game = search_game_info(result[0]['name'])
                if not rel_game is None:
                    rel_game_list.append(rel_game)
    # related_details = []
    # for related_game_name in res["hits"]["hits"][0]["_source"]["source"]["also_like"]:
    #     body = {
    #        "_source": {
    #             "includes": [
    #                 "source.name"
    #             ]
    #         },
    #         "query": {
    #             "bool": {
    #                 "must": {
    #                     "match": {
    #                         "source.name": related_game_name
    #                     }
    #                 }
    #             }
    #         }
    #     }
    #     relate_detail = es.search(
    #         index="videogames", 
    #         doc_type="game",
    #         body=body
    #     )
    #     if len(relate_detail["hits"]["hits"]) > 0:
    #         elem = {}
    #         elem["name"] = relate_detail["hits"]["hits"][0]["_source"]["source"]["name"]
    #         elem["id"] = relate_detail["hits"]["hits"][0]["_id"]
    #         related_details.append(elem)
         
    # return jsonify(res.hits.hits[0]._source.source)
    return render_template("details.html", game_info = game_info_dict, related_games = rel_game_list)

def search_game_info(game_name):
    body = {
        "from": 0,
        "size": 10,
        "query": {
            "bool": {
                "must": [{
                    "match": {"name": game_name}
                }]  
            }
        }
    }

    res = es.search(
        index="games", 
        body=body)
    
    if len(res['hits']['hits']) > 0:
        return res['hits']['hits'][0]
    else:
        return None

def clear_resource():
    if not driver is None:
        driver.close()

# atexit.register(clear_resource)    
app.run(debug = True)