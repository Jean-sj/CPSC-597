import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests


def find_elements(wd):
    elements = wd.find_elements(By.XPATH, "//img[@srcset]")
    return elements


def save_image(elements):
    for element in elements:
        # NBA 2K22 for Xbox One
        game_name = element.get_attribute('alt')

        save_path = "./ps4/" + game_name.replace("/", "#") + ".jpg"
        url = element.get_attribute('src')
        r = requests.get(url, stream=True)
        with open(save_path, 'wb') as fd:
            for chunk in r.iter_content():
                fd.write(chunk)


if __name__ == "__main__":
    wd = webdriver.Chrome()
    url = 'https://store.playstation.com/en-us/pages/browse'
    wd.get(url)

    time.sleep(5)
    wd.implicitly_wait(10)

    max_pages_number = int(wd.find_elements(By.XPATH, "//span[@class='psw-fill-x ']")[-1].text)
    print(max_pages_number)

    for i in range(max_pages_number):
        elements = find_elements(wd)
        save_image(elements)

        # check if it is the last page
        if i == max_pages_number - 1:
            break

        # go to next page
        next_url = url + "/" + str(i + 2)
        wd.get(next_url)
        time.sleep(2)

    wd.quit()
