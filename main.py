from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import pymysql
import time
import sys


def get_table(driver, cur, conn):
    driver.find_element(By.ID, 'btnSearch').click()
    time.sleep(3)

    table = driver.find_element(By.ID, 'gridLecture')
    rows = table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')
    for i in range(len(rows)):
        td = rows[i].find_elements(By.TAG_NAME, 'td')
        if len(td) < 2:
            return
        cur.execute("INSERT INTO course (campus, courseID, subID, division, department, courseName, professor) VALUES(%s, %s, %s, %s, %s, %s, %s)",
                    (td[0].text, td[1].text, td[2].text, td[3].text, td[4].text, td[5].text, td[6].text))
        for j in range(7):
            sys.stdout.write(td[j].text + " ")
        td[1].click()

        handles = driver.window_handles
        driver.switch_to.window(handles[-1])

        # check books
        driver.switch_to.frame('myiframe3')
        book_table = driver.find_element(By.XPATH, '/html/body/div/div/form/table')
        cur.execute("SELECT MAX(ID) FROM course")
        res = cur.fetchall()

        tb = book_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')
        if len(tb) == 0:
            sys.stdout.write("Check file {} \n".format(res[-1][-1]))
            try:
                driver.switch_to.parent_frame()
                file = driver.find_element(By.XPATH, '/html/body/div/div[2]/form[1]/table[5]/tbody/tr[2]/td[2]/a')
                file.click()
            except exceptions.NoSuchElementException:
                sys.stdout.write("No file {} \n".format(res[-1][-1]))
        else:
            for i in range(len(tb)):
                booktd = tb[i].find_elements(By.TAG_NAME, 'td')
                print(booktd[0].text)
                if booktd[4].text == '':
                    cur.execute("INSERT INTO book (courseID, bookname, author, published) VALUES(%s, %s, %s, %s)",
                                (res[-1][-1], booktd[1].text, booktd[2].text, 0))
                else:
                    cur.execute("INSERT INTO book (courseID, bookname, author, published) VALUES(%s, %s, %s, %s)",
                                (res[-1][-1], booktd[1].text, booktd[2].text, booktd[4].text))

                for j in range(len(booktd)):
                    sys.stdout.write(booktd[j].text+" ")
                sys.stdout.write("\n")

        time.sleep(2)
        driver.close()

        driver.switch_to.window(handles[0])
        driver.switch_to.frame("Main")
        driver.switch_to.frame("coreMain")
    conn.commit()


# Options
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
    "download.default_directory": r"G:\자료파일\고려대(세종)\3학년 2학기\캡스톤 디자인2\downloads",
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

# connect MySQL
conn = pymysql.connect(host='127.0.0.1', user='root', password='2038094', db='courseDB', charset='utf8')
cur = conn.cursor()

# search table information
category1 = Select(driver.find_element(By.ID, 'pCourDiv'))
for i in range(len(category1.options)):
    category1.select_by_index(i)
    time.sleep(2)
    if i < 2:
        category2 = Select(driver.find_element(By.ID, 'pCol'))
        category3 = Select(driver.find_element(By.ID, 'pDept'))
        for j in range(3, len(category2.options)):
            category2.select_by_index(j)
            driver.implicitly_wait(2)
            for k in range(len(category3.options)):
                category3.select_by_index(k)
                print(category1.all_selected_options[0].text,
                      category2.all_selected_options[0].text,
                      category3.all_selected_options[0].text)
                get_table(driver, cur, conn)
    elif i == 2:
        category2 = Select(driver.find_element(By.ID, 'pGroupCd'))
        for j in range(len(category2.options)):
            category2.select_by_index(j)
            print(category1.all_selected_options[0].text,
                  category2.all_selected_options[0].text)
            get_table(driver, cur, conn)
    else:
        print(category1.all_selected_options[0].text)
        get_table(driver, cur, conn)


# close
time.sleep(3)
driver.close()
conn.close()
