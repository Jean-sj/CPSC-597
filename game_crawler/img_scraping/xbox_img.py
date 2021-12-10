import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests


def find_elements(wd):
    elements = wd.find_elements(By.XPATH, "//picture[@class='containerIMG']/img[@alt!='game pass icon']")
    return elements


def save_image(elements):
    for element in elements:
        # box shot of NBA 2K22 for Xbox One
        # NBA 2K22 for Xbox One
        game_name = element.get_attribute('alt')[12:]

        save_path = "./xbox/" + game_name.replace("/", "#") + ".jpg"
        url = element.get_attribute('src')
        r = requests.get(url, stream=True)
        with open(save_path, 'wb') as fd:
            for chunk in r.iter_content():
                fd.write(chunk)


if __name__ == "__main__":
    wd = webdriver.Chrome()
    wd.get('https://www.xbox.com/en-us/games/all-games?cat=all')

    time.sleep(5)
    wd.implicitly_wait(10)

    pages = wd.find_elements(By.XPATH, '//nav//li[@data-label]/a')
    max_pages_number = len(pages)

    for i in range(max_pages_number):
        elements = find_elements(wd)
        save_image(elements)

        # check if it is the last page
        if i == max_pages_number - 1:
            break

        # go to next page
        wd.execute_script("arguments[0].click();", pages[i+1])
        time.sleep(2)

    wd.quit()
