import pymongo
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time



publisher_root_url = "https://en.wikipedia.org/wiki/List_of_video_game_publishers"

mongo_client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
gamedb = mongo_client["gamedb"]
developers_col = gamedb["publishers"]

def insert_developer(info_items, bg_str):
    # publisher name
    name = info_items[0].text.lower()  
    # City & country
    location = info_items[1].text.lower()
    location_arr = location.split(',')
    city = ""
    country = ""
    if len(location_arr) == 1:
        country = location_arr[0].strip().lower()
    elif len(location_arr) == 2:
        city = location_arr[0].strip().lower()
        country = location_arr[1].strip().lower()
    elif len(location_arr) == 3:
        city = location_arr[0].strip().lower()
        country = location_arr[2].strip().lower()    
    # Est. year
    est_year = info_items[2].text.lower()
    # Notes
    notes = info_items[4].text.lower()
    #status
    status = ''
    if bg_str == 'rgba(255, 232, 169, 1)':
        status = 'inactive'
    elif bg_str == 'rgba(0, 0, 0, 0)':
        status = 'independent'
    elif bg_str == 'rgba(201, 218, 255, 1)':
        status = 'subsidiary'
    
    developer_dict = {"name": name, "city": city, "country": country, 
        "est_year": est_year, "notes": notes, "status": status}

    developers_col.insert_one(developer_dict)

try:
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(publisher_root_url)
    time.sleep(2)

    all_developers_info = driver.find_elements_by_xpath("//table[contains(@class,'wikitable') and contains(@class,'sortable') and contains(@class,'jquery-tablesorter')]/tbody/tr")
    for developer_info in all_developers_info:
        # style = developer_info.get_attribute('style')
        back_color = developer_info.value_of_css_property('background-color')
        info_items = developer_info.find_elements_by_tag_name('td')
        if len(info_items) != 5:
            continue

        # developer name
        name = info_items[0].text.lower()
        if developers_col.find({"name": name}).count() == 0:
            insert_developer(info_items, back_color)

except Exception as e:
    print(e)
    mongo_client.close()

print("finished!")
mongo_client.close()
