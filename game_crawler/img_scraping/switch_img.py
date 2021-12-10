import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests


def save_image(url, game_name):
        save_path = "./switch/" + game_name.replace("/", "#") + ".jpg"
        r = requests.get(url, stream=True)
        with open(save_path, 'wb') as fd:
            for chunk in r.iter_content():
                fd.write(chunk)


if __name__ == "__main__":
    wd = webdriver.Chrome()
    wd.get('https://www.nintendo.com/games/game-guide/')

    time.sleep(5)
    wd.implicitly_wait(10)

    original_elements_number = len(wd.find_elements(By.XPATH, '//game-tile'))

    # load all the pages
    while True:
        load_more_elements_list = wd.find_elements(By.XPATH, '//styled-button[@id="btn-load-more"]')

        wd.execute_script("arguments[0].click();", load_more_elements_list[0])
        time.sleep(2)

        new_elements_number = len(wd.find_elements(By.XPATH, '//game-tile'))
        if original_elements_number == new_elements_number:
            break
        original_elements_number = new_elements_number

    elements_img_path = wd.find_elements(By.XPATH, '//game-tile')
    elements_img_name = wd.find_elements(By.XPATH, '//game-tile/h3')
    max_number_elements = len(elements_img_path)

    for i in range(max_number_elements):
        game_name = elements_img_name[i].text
        game_url = elements_img_path[i].get_attribute('image')
        save_image(game_url, game_name)

    wd.quit()
