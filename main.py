import sys
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
import index_ui, dataInput_ui, tag_ui, progress_ui, work
from PyQt5.QtWidgets import *

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



# work.Work("").run()



