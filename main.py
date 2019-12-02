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
print("mode:",mode)
ui_data={};
if(mode==1):
    ui_data=dataInput_ui.DataInputUI().run()
    app = QApplication(sys.argv)
    window = progress_ui.ProgressUI()
    sys.exit(app.exec_())
elif(mode==2):
    ui_data=tag_ui.TagUI().run()





