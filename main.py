import sys
import os
import index_ui, dataInput_ui, tag_ui, progress_ui, work, delete, progress_ui_delete, work_delete
from PyQt5.QtWidgets import *
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

ui=index_ui.IndexUI()
mode=ui.run()
ui_data={}
if(mode==1):
    ui_data=dataInput_ui.DataInputUI().run()
    if len(ui_data)!=0:
        app = QApplication(sys.argv)
        window = progress_ui.ProgressUI(ui_data)
        app.exec_()
        for file in os.scandir(os.getcwd() + '/pic'):
            os.remove(file.path)
elif(mode==2):
    ui_data=tag_ui.TagUI().run()
elif(mode==3):
    print("here")
    ui_data=delete.DataInputUI().run()
    print(ui_data)
    if len(ui_data)!=0:
        app = QApplication(sys.argv)
        window = progress_ui_delete.ProgressUI(ui_data)
        app.exec_()

# work.Work({"KEYWORD":"조아짐 강동구","ID":"manager3","PW":"manager3","ADD_CNT":4}).run()
# work_delete.Work({"ID":"manager3","PW":"manager3"}).run()
# progress_ui_delete.ProgressUIt("").run()

# site = "http://dmonster874.cafe24.com/bbs/login.php?url=http%3A%2F%2Fdmonster874.cafe24.com%2F"
#
# driver = webdriver.Chrome(os.getcwd() + '/chromedriver.exe')
# driver.set_page_load_timeout(100)
# driver.get(site)
# driver.implicitly_wait(3)
#
# id_box = driver.find_element_by_id('login_id')
# pw_box = driver.find_element_by_id('login_pw')
# login_btn = driver.find_element_by_class_name('btn_submit')
# ActionChains(driver).send_keys_to_element(id_box, "manager3").send_keys_to_element(pw_box,
#                                                                                                "manager3").click(
#                 login_btn).perform()
# admin_btn = driver.find_elements_by_tag_name('a')
# ActionChains(driver).click(admin_btn[3]).perform()
# driver.implicitly_wait(3)
# input_tag = driver.find_element_by_class_name('frm_input')
# driver.execute_script("arguments[0].setAttribute('value',arguments[1])", input_tag, "테스트")
# input_tag.send_keys(Keys.ENTER)
# tr=driver.find_elements_by_css_selector('tbody>tr')
# print(tr)
#
# time.sleep(3)
# select_tags=driver.find_elements_by_css_selector('#chk_flag>option')[2].click()
# time.sleep(3)
# tr2=driver.find_elements_by_css_selector('tbody>tr')
# print(tr2)








