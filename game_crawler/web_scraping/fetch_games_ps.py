import pymongo
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


playstation_4_list = ["https://en.wikipedia.org/wiki/List_of_PlayStation_4_games", \
    "https://en.wikipedia.org/wiki/List_of_PlayStation_4_games_(M%E2%80%93Z)"]

xbox_one_list = ["https://en.wikipedia.org/wiki/List_of_Xbox_One_games_(A%E2%80%93L)", \
    "https://en.wikipedia.org/wiki/List_of_Xbox_One_games_(M%E2%80%93Z)"]

def insert_game(info_items):
    # game name
    name = info_items[0].text.lower()   
    # genre(s)
    genres = []
    genres_items = info_items[1].find_elements_by_tag_name('li')
    if len(genres_items) == 0:
        genres.append(info_items[1].text.lower())
    else:
        for genre_item in genres_items:
            genres.append(genre_item.text.lower())
    # developer(s)
    developers = []
    developers_items = info_items[2].find_elements_by_tag_name('li')
    if len(developers_items) == 0:
        developers.append(info_items[2].text.lower())
    else:
        for developer_item in developers_items:
            developers.append(developer_item.text.lower())
    # publisher(s)
    publishers = []
    publishers_item = info_items[3].find_elements_by_tag_name('li')
    if len(publishers_item) == 0:
        publishers.append(info_items[3].text.lower())
    else:
        for publisher_item in publishers_item:
            publishers.append(publisher_item.text.lower())
    # release date
    # convert to date type, save for later use
    # release_date = {}
    # release JP
    release_JP = info_items[4].text
    # release NA
    release_NA = info_items[5].text
    # release PAL
    release_PAL = info_items[6].text

    release_date = {"JP" : release_JP, "NA": release_NA, "PAL": release_PAL}

    # overall
    game_dict = { "name": name, "genres": genres, "developers": developers, "publishers": publishers, 
                    "releaseDate": { "xbox one": release_date }, "platform": ["xbox one"]}
    games_col.insert_one(game_dict)

def update_game(info_items):
    #name
    name = info_items[0].text.lower()   
    # release date
    # release JP
    release_JP = info_items[4].text
    # release NA
    release_NA = info_items[5].text
    # release PAL
    release_PAL = info_items[6].text

    release_date = {"JP" : release_JP, "NA": release_NA, "PAL": release_PAL}

    games_col.find_one_and_update({"name": name}, {"$set": {"releaseDate.xbox one": release_date}, "$push": {"platform": "xbox one"}})


mongo_client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
gamedb = mongo_client["gamedb"]
games_col = gamedb["games"]


try:
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(xbox_one_list[1])
    time.sleep(2)

    all_games_info = driver.find_elements_by_xpath("//table[@id='softwarelist']/tbody/tr")

    for game_info in all_games_info:
        info_items = game_info.find_elements_by_tag_name('td')
        if len(info_items) != 9:
            continue        
        # game name
        name = info_items[0].text.lower()
        if games_col.find({"name": name}).count() == 0:
            insert_game(info_items)
        else:
            update_game(info_items)
except Exception as e:
    print(e)
    mongo_client.close()

print("finished!")
mongo_client.close()



