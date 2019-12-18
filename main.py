import sys
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


# work.Work({"KEYWORD":"스타짐 서면점","ID":"manager3","PW":"manager3","ADD_CNT":4}).run()



