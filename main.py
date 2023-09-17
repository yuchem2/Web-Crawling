from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import time
import sys


def get_table(driver):
    driver.find_element(By.ID, 'btnSearch').click()
    time.sleep(3)

    table = driver.find_element(By.ID, 'gridLecture')
    rows = table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')

    for i in range(len(rows)):
        td = rows[i].find_elements(By.TAG_NAME, 'td')
        for j in range(7):
            sys.stdout.write(td[j].text+" ")
        sys.stdout.write("\n")
        td[1].click()

        handles = driver.window_handles
        driver.switch_to.window(handles[-1])

        # check books
        driver.switch_to.frame('myiframe3')
        book_table = driver.find_element(By.XPATH, '/html/body/div/div/form/table')
        try:
            tb = book_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')
            for i in range(len(tb)):
                td = tb[i].find_elements(By.TAG_NAME, 'td')
                for j in range(len(td)):
                    print(td[j].text, end=" ")
                print()

        except exceptions.NoSuchElementException:
            pass
        finally:
            driver.switch_to.parent_frame()
            file = driver.find_element(By.XPATH, '/html/body/div/div[2]/form[1]/table[5]/tbody/tr[2]/td[2]/a')
            file.click()
            time.sleep(2)
            driver.close()

        driver.switch_to.window(handles[0])
        driver.switch_to.frame("Main")
        driver.switch_to.frame("coreMain")


# Options
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
    "download.default_directory": r"G:\자료파일\고려대(세종)\3학년 2학기\캡스톤 디자인2\Web Crawling\downloads",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowing.enabled": True
})

# loading web
driver = webdriver.Chrome(options=options)

driver.implicitly_wait(2)
driver.get("https://sugang.korea.ac.kr/")
driver.switch_to.frame("Main")

driver.find_element(By.CLASS_NAME, "jconfirm-closeIcon").click()
driver.find_element(By.ID, "menu_hakbu").click()

driver.implicitly_wait(2)
driver.switch_to.frame("coreMain")

# category select
campus = Select(driver.find_element(By.XPATH, '//*[@id="pCampus"]'))
campus.select_by_value("2")

category1 = Select(driver.find_element(By.ID, 'pCourDiv'))
for i in range(len(category1.options)):
    category1.select_by_index(i)
    time.sleep(2)
    if i < 2:
        category2 = Select(driver.find_element(By.ID, 'pCol'))
        category3 = Select(driver.find_element(By.ID, 'pDept'))
        for j in range(len(category2.options)):
            category2.select_by_index(j)
            driver.implicitly_wait(2)
            for k in range(len(category3.options)):
                category3.select_by_index(k)
                print(category1.all_selected_options[0].text,
                      category2.all_selected_options[0].text,
                      category3.all_selected_options[0].text)
                get_table(driver)
    elif i == 2:
        category2 = Select(driver.find_element(By.ID, 'pGroupCd'))
        for j in range(len(category2.options)):
            category2.select_by_index(j)
            print(category1.all_selected_options[0].text,
                  category2.all_selected_options[0].text)
            get_table(driver)
    else:
        print(category1.all_selected_options[0].text)
        get_table(driver)
    break


time.sleep(3)
