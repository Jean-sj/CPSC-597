
import pymongo
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


nintendo_switch_list = ["https://en.wikipedia.org/wiki/List_of_Nintendo_Switch_games_(A%E2%80%93C)", \
    "https://en.wikipedia.org/wiki/List_of_Nintendo_Switch_games_(D%E2%80%93G)", \
    "https://en.wikipedia.org/wiki/List_of_Nintendo_Switch_games_(H%E2%80%93P)", \
    "https://en.wikipedia.org/wiki/List_of_Nintendo_Switch_games_(Q%E2%80%93Z)"]

def insert_game(info_items, name):
    # genre(s)
    genres = []
    genres_items = info_items[0].find_elements_by_tag_name('li')
    if len(genres_items) == 0:
        genres.append(info_items[0].text.lower())
    else:
        for genre_item in genres_items:
            genres.append(genre_item.text.lower())
    # developer(s)
    developers = []
    developers_items = info_items[1].find_elements_by_tag_name('li')
    if len(developers_items) == 0:
        developers.append(info_items[1].text.lower())
    else:
        for developer_item in developers_items:
            developers.append(developer_item.text.lower())
    # publisher(s)
    publishers = []
    publishers_item = info_items[2].find_elements_by_tag_name('li')
    if len(publishers_item) == 0:
        publishers.append(info_items[2].text.lower())
    else:
        for publisher_item in publishers_item:
            publishers.append(publisher_item.text.lower())
    # release date
    # convert to date type, save for later use
    # release_date = {}
    # release JP
    release_JP = info_items[3].text
    # release NA
    release_NA = info_items[4].text
    # release PAL
    release_PAL = info_items[5].text

    release_date = {"JP" : release_JP, "NA": release_NA, "PAL": release_PAL}

    # overall
    game_dict = { "name": name, "genres": genres, "developers": developers, "publishers": publishers, 
                    "releaseDate": { "nintendo switch": release_date }, "platform": ["nintendo switch"]}
    games_col.insert_one(game_dict)

def update_game(info_items, name):  
    # release date
    # release JP
    release_JP = info_items[3].text
    # release NA
    release_NA = info_items[4].text
    # release PAL
    release_PAL = info_items[5].text

    release_date = {"JP" : release_JP, "NA": release_NA, "PAL": release_PAL}

    games_col.find_one_and_update({"name": name}, {"$set": {"releaseDate.nintendo switch": release_date}, "$push": {"platform": "nintendo switch"}})


mongo_client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
gamedb = mongo_client["gamedb"]
games_col = gamedb["games"]


try:
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(nintendo_switch_list[3])
    time.sleep(2)

    all_games_info = driver.find_elements_by_xpath("//table[@id='softwarelist']/tbody/tr")

    for game_info in all_games_info:
        title_item = game_info.find_elements_by_tag_name('th')
        info_items = game_info.find_elements_by_tag_name('td')
        if len(info_items) != 7 and len(title_item) != 1:
            continue  
        # game name
        name = title_item[0].text.lower()
        if games_col.find({"name": name}).count() == 0:
            insert_game(info_items, name)
        else:
            update_game(info_items, name)
except Exception as e:
    print(e)
    mongo_client.close()

print("finished!")
mongo_client.close()