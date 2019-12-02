
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

class Work(QThread):
    countChanged = pyqtSignal(int)
    logChanged = pyqtSignal("PyQt_PyObject")
    insertChanged = pyqtSignal("PyQt_PyObject")
    log="null"
    inserted="null"
    qcnt = 0
    file_name = 0
    page_num = 0
    cnt = 0
    flag = True
    out = False
    received_data_cnt = 0
    id_list = []
    data_list = []
    correct = ['스피닝', '수영', '줌바', '에어로빅', 'G.X', 'GX', 'G.T', 'GT', '프리패스', '요가', '필라테스', '골프', 'PT', 'pt',
               '피티', '댄스', '스쿼시', '전종목'
        , '헬스 + G.X', '헬스 + 골프', '헬스 + G.X + 골프', '크로스핏', '헬스 + G.T', '헬스 + 요가 + 필라테스', '헬스 + 스쿼시', '헬스 + 스피닝',
               '헬스(야간)', '헬스 + PT']
    def run(self):

        while True:
            self.countChanged.emit(self.qcnt)

            options = Options()
            options.add_argument("--start-maximized")
            driver = webdriver.Chrome(os.getcwd() + '/chromedriver', options=options)
            driver.implicitly_wait(3)


            # keyword = "대전광역시 헬스장"
            keyword = "스포애니 강남역 1호점"
            self.fun1(keyword,driver)

            print("searched data : " + str(len(self.data_list)))
            print(self.data_list)
            # gym site inesert

            site = "http://dmonster874.cafe24.com/bbs/login.php?url=http%3A%2F%2Fdmonster874.cafe24.com%2F"
            options = Options()
            options.add_argument("--start-maximized")
            driver = webdriver.Chrome(os.getcwd() + '/chromedriver', options=options)
            driver.set_page_load_timeout(100)
            driver.get(site)
            driver.implicitly_wait(3)

            id_box = driver.find_element_by_id('login_id')
            pw_box = driver.find_element_by_id('login_pw')
            login_btn = driver.find_element_by_class_name('btn_submit')
            ActionChains(driver).send_keys_to_element(id_box, 'manager3').send_keys_to_element(pw_box,
                                                                                               'manager3').click(
                login_btn).perform()
            admin_btn = driver.find_elements_by_tag_name('a')
            ActionChains(driver).click(admin_btn[3]).perform()
            driver.implicitly_wait(3)

            show2 = 0
            for abc in range(0, len(self.data_list)):
                print(self.data_list[abc]['title'])
                self.insert_data(self.data_list[abc],driver)
                self.click_submit(driver)
                try:
                    WebDriverWait(driver, 100).until(EC.alert_is_present(),
                                                     'Timed out waiting for PA creation ' + 'confirmation popup to appear.')
                    inserted=" --- 입력 완료"
                    self.insertChanged.emit(inserted)
                except:
                    print("time out !!")
                    inserted=" 입력 실패"
                    self.insertChanged.emit(inserted)
                    driver.refresh();
                    abc = abc - 1
                    self.out = True
                    continue
                art = driver.switch_to.alert
                art.accept()
                driver.switch_to.default_content()
                time.sleep(2)
                self.qcnt = (abc + 1) / len(self.data_list) * 100
                self.countChanged.emit(self.qcnt)
                print(show2)
                show2 = show2 + 1

            break
            ##파일저장
            # url="http://ldb.phinf.naver.net/20160322_64/1458654453155zVjxg_JPEG/176272627752929_0.jpeg"
            # myfile = requests.get(url)
            # open('/home/jung/다운로드/abc.jpeg', 'wb').write(myfile.content)

    def fun1(self,keyword,driver):
        URL = "https://map.naver.com/?query=" + keyword + "&type=SITE_1&queryRank=0"
        driver.get(URL)
        driver.implicitly_wait(10)

        self.get_all_data(driver)

    def get_all_data(self,driver):
        time.sleep(3)
        self.collect_page(driver)
        while True:
            flag = self.next_page_click(driver)
            if not flag:
                break
            time.sleep(1)
            self.collect_page(driver)

    def collect_page(self,driver):
        notices = driver.find_elements_by_css_selector('div.title_box')
        # print(notices)
        ActionChains(driver).click(notices[0]).perform()
        for tmp in notices:
            ActionChains(driver).click(tmp).perform()
            self.collect_one_data(driver)
            time.sleep(3)
            driver.back()

    def collect_one_data(self,driver):
        time.sleep(3)
        # 제목
        title = driver.find_element_by_class_name('summary_title').text
        # 더보기 누르기
        more_btn = driver.find_elements_by_class_name('btn_more')
        if len(more_btn) != 0:
            for tmp in more_btn:
                ActionChains(driver).click(tmp).perform()
        # 주소
        address = []
        ad_tag = driver.find_elements_by_css_selector('a.end_title')
        if len(ad_tag) != 0:
            address.append(ad_tag[0].text)
        # 전화번호
        phone = []
        ph_tag = driver.find_elements_by_css_selector('div.phone>div.end_box>a.link_end')
        if len(ph_tag) != 0:
            phone.append(ph_tag[0].text)
        # 시간
        part = []
        times = driver.find_elements_by_css_selector('li.item_business')
        if len(times) != 0:
            for tmp in times:
                part.append(tmp.text)
        # 가격
        prices = []
        price_tags = driver.find_elements_by_css_selector('div.menu>div.end_box>ul.list_menu>li.item_menu')
        if len(price_tags) != 0:
            for tmp in price_tags:
                prices.append(tmp.text)
        # 세부내용
        details = []
        detail_tag = driver.find_elements_by_css_selector('div.detail>div.end_box')
        if len(detail_tag) != 0:
            details.append(detail_tag[0].text)
        # 사진
        pic_tag = driver.find_elements_by_css_selector('div.link_thumb>img')
        images = []
        if len(pic_tag) != 0:
            ActionChains(driver).click(pic_tag[0]).perform()
            pic_list = driver.find_elements_by_css_selector('li.item_photo>a>img')
            for tmp in pic_list:
                images.append(tmp.get_attribute('src'))
            driver.back()
        # 데이터 만들기
        data = {}
        data['images'] = images
        data['title'] = title
        data['types'] = ""
        data['address'] = address
        data['times'] = part
        data['phone'] = phone
        data['prices'] = prices
        data['details'] = details
        print(data)
        log=data['title']
        self.logChanged.emit(log)
        self.data_list.append(data)

    def next_page_click(self,driver):
        page = driver.find_elements_by_css_selector('button.btn_next')
        try:
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn_next")))
        except:
            return False
        ActionChains(driver).click(page[self.page_num]).perform()
        return True

    def insert_data(self,data,driver):
        # 추가 누르기
        if self.out != True:
            time.sleep(10)
            add_btn = driver.find_element_by_class_name('btn_insert')
            ActionChains(driver).click(add_btn).perform()
        else:
            self.out = False
        # 사진
        ele = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.NAME, 'bf_file[]')))
        ele[0].send_keys(os.getcwd() + '/No_Picture.jpg')
        # pic_cnt = len(data['images'])
        # for i in range(1, 20 if pic_cnt > 20 else pic_cnt):
        #     self.add_pic_box(pic_cnt,driver)
        # picture = WebDriverWait(driver, 60).until(
        #     EC.presence_of_all_elements_located((By.CLASS_NAME, 'reg_file')))
        # ele = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.NAME, 'bf_file[]')))
        # if pic_cnt == 0:
        #     ele[0].send_keys(os.getcwd() + '/No_Picture.jpg')
        # elif pic_cnt == 1 and data['images'][0] == None:
        #     ele[0].send_keys(os.getcwd() + '/No_Picture.jpg')
        # else:
        #     for i in range(0, 20 if pic_cnt > 20 else pic_cnt):
        #         pic_url = data['images'][i]
        #         response = requests.get(pic_url)
        #         self.file_name = self.file_name + 1;
        #         open(os.getcwd() + '/pic/' + str(self.file_name) + '.jpeg', 'wb').write(response.content)
        #         time.sleep(4)
        #         ele[i].send_keys(os.getcwd() + '/pic/' + str(self.file_name) + '.jpeg')
        #         str1 = "background-image: url('" + pic_url + "'); background-size: cover; opacity: 1;"
        #         driver.execute_script("arguments[0].setAttribute('style',arguments[1])", picture[i], str1)
        #         driver.execute_script("arguments[0].setAttribute('class','reg_file on')", picture[i])
        # 제목
        title = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, 'g_name')))
        ActionChains(driver).send_keys_to_element(title, data['title']).perform()

        # 위치
        iframe = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'iframe')))
        driver.switch_to.frame(iframe[0])
        locate = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, 'gym_keyword')))
        add = ""
        str_tmp = data['address'][0].split(" ")
        for idx in range(0, 4 if len(str_tmp) > 4 else len(str_tmp)):
            add = add + str_tmp[idx] + " "
        ActionChains(driver).send_keys_to_element(locate, add).perform()
        ActionChains(driver).click(driver.find_element_by_class_name('btn_search')).perform()
        tmp_tag = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, 'placesList'))).find_elements_by_tag_name('li')
        if len(tmp_tag) != 0:
            tf = False
            pg = driver.find_elements_by_css_selector('#pagination>a')
            pg_size = len(pg)
            for j in range(0, pg_size):
                pg = driver.find_elements_by_css_selector('#pagination>a')
                ActionChains(driver).click(pg[j]).perform()
                time.sleep(1)
                tags = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'h5')))
                stop = False
                for k in range(0, len(tags)):
                    if tags[k].text.find(data['title']) != -1:
                        tf = True
                        ActionChains(driver).click(tags[k]).perform()
                        stop = True
                        break;
                if stop:
                    break;
            if not tf:
                ActionChains(driver).click(tmp_tag[0]).perform()
        driver.switch_to.default_content()
        time.sleep(1)

        # 세부내용 + 가격
        texts = ""
        price_size = len(data['prices'])
        if price_size != 0:
            for ttm in data['prices']:
                tmp = ttm.split('\n')
                texts = texts + tmp[1] + " : " + tmp[0] + "\n"
            texts = texts + "\n\n"
        if len(data['details']) != 0:
            texts = texts + data['details'][0]
        # 종목
        type_add = WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'btn_add')))
        ActionChains(driver).click(type_add[1]).perform()
        type_cnt = 1
        index = 1
        if len(texts) != 0:
            pressed_details = texts.replace(" ", "")
            for tmp in self.correct:
                k = tmp.replace(" ", "")
                if pressed_details.find(k) != -1:
                    if type_cnt == 9:
                        break
                    type_add = WebDriverWait(driver, 60).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, 'btn_add')))
                    ActionChains(driver).click(type_add[1]).perform()
                    type_cnt = type_cnt + 1
                    scroll = driver.find_element_by_name(
                        'g_category[' + str(index) + ']').find_elements_by_tag_name('option')
                    for j in range(0, len(scroll)):
                        if scroll[j].text == tmp:
                            driver.execute_script("arguments[0].setAttribute('selected','')", scroll[j])
                            break
                    index = index + 1

        time.sleep(1)
        # 이용시간
        use_time1 = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, 'use_hours_0')))
        use_time2 = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, 'use_hours_1')))
        use_time3 = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, 'use_hours_2')))
        mon_text = ""
        sat_text = ""
        hol_text = ""
        for i in range(0, len(data['times'])):
            temp = data['times'][i].split()
            if temp[0] == '평일':
                mon_text = mon_text + temp[1]
            elif temp[1] == '휴관' or temp[1] == '휴무':
                if hol_text != "":
                    hol_text = hol_text + " / "
                hol_text = hol_text + temp[0]
            else:
                if sat_text != "":
                    sat_text = sat_text + " / "
                sat_text = sat_text + temp[0] + " : " + temp[1]
        if mon_text == "":
            mon_text = "X"
        if sat_text == "":
            sat_text = "X"
        if hol_text == "":
            hol_text = "X"
        ActionChains(driver).send_keys_to_element(use_time1, mon_text).perform()
        ActionChains(driver).send_keys_to_element(use_time2, sat_text).perform()
        ActionChains(driver).send_keys_to_element(use_time3, hol_text).perform()

        # 전화번호
        if len(data['phone']) != 0:
            phone = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, 'g_hp')))
            ActionChains(driver).send_keys_to_element(phone, data['phone'][0]).perform()
        time.sleep(1)
        # 세부내용
        driver.switch_to.frame(iframe[1])
        detail = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'se2_input_wysiwyg')))
        if texts == "":
            texts = "X"
        ActionChains(driver).send_keys_to_element(detail, texts).perform()
        driver.switch_to.default_content()
        time.sleep(3)

    def add_pic_box(self,cnt,driver):
        tag = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'td')))
        pic_cnt = 1
        tt = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, 'cnt_file')))
        if cnt > 20:
            cnt = 20
        driver.execute_script("arguments[0].setAttribute('value',arguments[1])", tt, cnt)
        str1 = '<div class="filebox wh1 multi">' \
               + '<input class="upload-name" value="파일선택" disabled="disabled">' \
               + '<label for="reg_file' + str(pic_cnt) + '" class="reg_file"></label>' \
               + '<input type="file" name="bf_file[]" id="reg_file' + str(
            pic_cnt) + '" class="upload-hidden" onchange="upload_preview(this);">' \
               + '<button type="button" class="del" title="삭제"></button>' \
               + '</div> '
        driver.execute_script("arguments[0].insertAdjacentHTML('beforeend',arguments[1])", tag[0], str1)

    def click_submit(self,driver):
        submit_btn = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'btn_submit')))
        ActionChains(driver).click(submit_btn).perform()

