
from selenium import webdriver
#from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.by import By
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import index_ui, dataInput_ui, tag_ui, progress_ui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal
from selenium.webdriver.common.keys import Keys

class Work(QThread):
    countChanged = pyqtSignal(int)
    logChanged = pyqtSignal("PyQt_PyObject")
    qcnt = 0
    input_data={}
    dataList=[]
    def __init__(self, ui_data):
        super().__init__()
        self.input_data=ui_data

    def run(self):
        while True:
            self.countChanged.emit(self.qcnt)

            # gym site inesert

            site = "http://dmonster874.cafe24.com/bbs/login.php?url=http%3A%2F%2Fdmonster874.cafe24.com%2F"
            options = Options()
            options.add_argument("--start-maximized")
            driver = webdriver.Chrome(os.getcwd() + '/chromedriver.exe', options=options)
            driver.set_page_load_timeout(100)
            driver.get(site)
            driver.implicitly_wait(3)

            id_box = driver.find_element_by_id('login_id')
            pw_box = driver.find_element_by_id('login_pw')
            login_btn = driver.find_element_by_class_name('btn_submit')
            ActionChains(driver).send_keys_to_element(id_box, self.input_data['ID']).send_keys_to_element(pw_box,
                                                                                               self.input_data['PW']).click(
                login_btn).perform()
            admin_btn = driver.find_elements_by_tag_name('a')
            ActionChains(driver).click(admin_btn[3]).perform()
            driver.implicitly_wait(3)

            self.compare_list(driver)
            print(len(self.dataList))
            driver.find_elements_by_css_selector('#chk_flag>option')[2].click()
            self.compare_list(driver)
            print(len(self.dataList))
            print(self.dataList)
            index=0
            for tmp in self.dataList:
                keyword=tmp['title']
                URL = "https://map.naver.com/v5/search/" + keyword
                driver.get(URL)
                driver.implicitly_wait(5)
                notices = driver.find_elements_by_css_selector('div.title_box')
                if len(notices)!=0:
                    ActionChains(driver).click(notices[0]).perform()
                else:
                    self.show_log(tmp)
                    index = index + 1
                    self.qcnt = (index) / len(self.dataList) * 100
                    self.countChanged.emit(self.qcnt)
                    continue
                flag=self.check_mode(driver)
                exist=False
                if flag:
                    print("first mode!")
                    exist=self.address_compare(driver,tmp)
                else:
                    print("sec mode!")
                    exist=self.collect_page(driver,tmp)
                    while not exist:
                        flag = self.next_page_click(driver)
                        if not flag:
                            break
                        time.sleep(1)
                        exist=self.collect_page(driver,tmp)
                if not exist:
                    self.show_log(tmp)
                time.sleep(2)
                index=index+1
                self.qcnt = (index) / len(self.dataList) * 100
                self.countChanged.emit(self.qcnt)
            break
    def collect_page(self,driver,tmp):
        time.sleep(1)
        notices = driver.find_elements_by_css_selector('div.title_box')
        exist=False
        for item in notices:
            ActionChains(driver).click(item).perform()
            exist = self.address_compare(driver, tmp)
            driver.back()
            if exist:
                break
        return exist
    def next_page_click(self,driver):
        page = driver.find_elements_by_css_selector('button.btn_next')
        try:
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn_next")))
        except:
            return False
        ActionChains(driver).click(page[0]).perform()
        return True

    def address_compare(self,driver,tmp):
        address = []
        ad_tag = driver.find_elements_by_css_selector('a.end_title')
        if len(ad_tag) != 0:
            address.append(ad_tag[0].text)
        print(address[0])
        print(tmp['address'])
        if address[0].replace(" ", "").find(tmp['address'].replace(" ", "")) != -1:
            return True
        return False
    def show_log(self,data):
        print("show_log in!")
        self.logChanged.emit(data['title'])

    def check_mode(self,driver):
        url=driver.current_url
        print(url)
        if url.find("place")!=-1:
            return True
        return False

    def compare_list(self,driver):
        flag=True
        cur_page_num=1
        while flag:
            WebDriverWait(driver, 60).until(EC.invisibility_of_element_located((By.ID, 'fancybox-loading')))
            tr = driver.find_elements_by_css_selector('tbody>tr')
            if len(tr)==0:
                return False
            for tmp in tr:
                data = {}
                title=tmp.find_element_by_css_selector('td.td_subject').text
                if title.find("(") != -1:
                    title=title.split("(")
                    data['title'] = title[0]
                else:
                    data['title'] = title
                address=tmp.find_elements_by_css_selector('td.td_num')[1].text
                if address.find(".")!=-1:
                    address=address.split(".")
                elif address.find("(")!=-1:
                    address = address.split("(")
                data['address']=address[0].rstrip('\n')
                self.dataList.append(data)
            flag=self.move_next_page(driver,cur_page_num)
            WebDriverWait(driver, 60).until(EC.invisibility_of_element_located((By.ID, 'fancybox-loading')))
            cur_page_num = cur_page_num + 1
            # break #테스트용
        return True

    def move_next_page(self,driver,cur_page_num):
        page_tags = driver.find_elements_by_css_selector('div.paging_wrap>li')
        for index in range(0,len(page_tags)):
            tmp=page_tags[index]
            if not tmp.text.isdigit():
                continue
            if int(tmp.text)==cur_page_num and index+1<len(page_tags):
                if not page_tags[index+1].text.isdigit():
                    continue
                else:
                    page_tags[index+1].click()
                    return True

        return False