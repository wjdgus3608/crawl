
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
import ui

#ui_data=ui.run().data
#print("UI data :",ui_data)

file_name=0
page_num = 0
cnt = 0
flag = True
out= False
total = 0
received_data_cnt = 0
end_page = 0
id_list = []
data_list = []
correct=['스피닝','수영','줌바','에어로빅','G.X','GX','G.T','GT','프리패스','요가','필라테스','골프','PT','pt','피티','댄스','스쿼시','전종목'
         ,'헬스 + G.X','헬스 + 골프','헬스 + G.X + 골프','크로스핏','헬스 + G.T','헬스 + 요가 + 필라테스','헬스 + 스쿼시','헬스 + 스피닝','헬스(야간)','헬스 + PT']


options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(os.getcwd()+'/chromedriver',options=options)
driver.implicitly_wait(3)


def fun1(keyword):
    URL = "https://map.naver.com/?query=" + keyword + "&type=SITE_1&queryRank=0"
    driver.get(URL)
    driver.implicitly_wait(10)

    get_all_data()
    print("data_list : ", id_list)
    print("data_list_size :", len(id_list))
    print("received data cnt : ", received_data_cnt)

def get_all_data():
    time.sleep(3)
    collect_page()
    while True:
        flag = next_page_click()
        if not flag:
            break
        time.sleep(1)
        collect_page()

def collect_page():
    global received_data_cnt
    notices = driver.find_elements_by_css_selector('div.title_box')
    #print(notices)
    ActionChains(driver).click(notices[0]).perform()
    for tmp in notices:
        ActionChains(driver).click(tmp).perform()
        collect_one_data()
        time.sleep(3)
        driver.back()

def collect_one_data():
    time.sleep(3)
    #제목
    title=driver.find_element_by_class_name('summary_title').text
    #더보기 누르기
    more_btn=driver.find_elements_by_class_name('btn_more')
    if len(more_btn)!=0:
        for tmp in more_btn:
            ActionChains(driver).click(tmp).perform()
    #주소
    address=[]
    ad_tag=driver.find_elements_by_css_selector('a.end_title')
    if len(ad_tag)!=0:
        address.append(ad_tag[0].text)
    #전화번호
    phone=[]
    ph_tag=driver.find_elements_by_css_selector('div.phone>div.end_box>a.link_end')
    if len(ph_tag)!=0:
        phone.append(ph_tag[0].text)
    #시간
    part = []
    times=driver.find_elements_by_css_selector('li.item_business')
    if len(times)!=0:
        for tmp in times:
            part.append(tmp.text)
    #가격
    prices = []
    price_tags=driver.find_elements_by_css_selector('div.menu>div.end_box>ul.list_menu>li.item_menu')
    if len(price_tags)!=0:
        for tmp in price_tags:
            prices.append(tmp.text)
    #세부내용
    details = []
    detail_tag=driver.find_elements_by_css_selector('div.detail>div.end_box')
    if len(detail_tag)!=0:
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
    #데이터 만들기
    data={}
    data['images'] = images
    data['title'] = title
    data['types'] = ""
    data['address'] = address
    data['times'] = part
    data['phone'] = phone
    data['prices'] = prices
    data['details'] = details
    print(data)
    data_list.append(data)

def next_page_click():
    global page_num, flag, cnt
    cnt = cnt + 1
    page = driver.find_elements_by_css_selector('button.btn_next')
    try:
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn_next")))
    except:
        return False
    ActionChains(driver).click(page[page_num]).perform()
    return True


def make_data():
    pictures_class =driver.find_elements_by_class_name('sp_thumb_lst')
    pictures=[]
    images=[]
    if len(pictures_class) != 0:
        if len(pictures_class) == 1:
            pictures = pictures_class[0].find_elements_by_tag_name('li>a>img')
        else:
            pictures = pictures_class[len(pictures_class) - 1].find_elements_by_tag_name('li>a>img')

    for picture in pictures:
        images.append(picture.get_attribute('data-origin'))
    title = driver.find_element_by_tag_name('h1').text
    tmp = driver.find_element_by_class_name('_siteviewAddress').text
    types=[]
    exer_types = []
    tmp_class=driver.find_elements_by_class_name('item_keyword')
    if len(tmp_class) !=0:
        types = tmp_class[0].find_elements_by_tag_name('a')
        for exer in types:
            exer_types.append(exer.text)
    ttest=tmp.split("지번",1)
    if len(ttest)!=1:
        address = tmp.split("지번", 1)[1].rstrip('\n')
    else:
        address=tmp
    phone_class = driver.find_elements_by_class_name('_siteviewPhone')
    phone=[]
    if len(phone_class) !=0 :
        phone.append(phone_class[0].text)
    use_class=driver.find_elements_by_class_name('section_detail_time')
    uses=[]
    times=[]
    if len(use_class) !=0:
        uses=use_class[0].find_elements_by_tag_name('ul>li')
        for use in uses:
            times.append(use.text)
    details = []
    prices=[]
    price_class=driver.find_elements_by_class_name('section_detail_pay ')
    if len(price_class) !=0:
        strongs=price_class[0].find_elements_by_tag_name('ul>li strong')
        for strong in strongs:
            prices.append(strong.text)
    detail_class=driver.find_elements_by_class_name('spm_t_detail')

    if len(detail_class) !=0:
        tt1=detail_class[0].find_element_by_xpath("./../..").find_element_by_tag_name('p')
        details.append(tt1.text)
    data={}
    data['images'] = images
    data['title']=title
    data['types'] = exer_types
    data['address'] = address
    data['times'] = times
    data['phone'] = phone
    data['prices']=prices
    data['details'] = details
    data_list.append(data)

def insert_data(data):
    global file_name, out
    #추가 누르기
    if out !=True:
        time.sleep(10)
        add_btn = driver.find_element_by_class_name('btn_insert')
        ActionChains(driver).click(add_btn).perform()
    else:
        out=False
    # 사진
    # pic_cnt=len(data['images'])
    # for i in range(1,20 if pic_cnt>20 else pic_cnt):
    #     add_pic_box(pic_cnt)
    # picture = WebDriverWait(driver,60).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'reg_file')))
    # ele = WebDriverWait(driver,60).until(EC.presence_of_all_elements_located((By.NAME,'bf_file[]')))
    # if pic_cnt==0:
    #     ele[0].send_keys(os.getcwd()+'/No_Picture.jpg')
    # elif pic_cnt==1 and data['images'][0]==None:
    #     ele[0].send_keys(os.getcwd()+'/No_Picture.jpg')
    # else:
    #     for i in range(0,20 if pic_cnt>20 else pic_cnt):
    #         pic_url = data['images'][i]
    #         response = requests.get(pic_url)
    #         file_name=file_name+1;
    #         open(os.getcwd()+'/pic/'+str(file_name)+'.jpeg', 'wb').write(response.content)
    #         time.sleep(4)
    #         ele[i].send_keys(os.getcwd()+'/pic/'+str(file_name)+'.jpeg')
    #         str1 = "background-image: url('" + pic_url + "'); background-size: cover; opacity: 1;"
    #         driver.execute_script("arguments[0].setAttribute('style',arguments[1])", picture[i], str1)
    #         driver.execute_script("arguments[0].setAttribute('class','reg_file on')", picture[i])
    #제목
    title =WebDriverWait(driver,60).until(EC.presence_of_element_located((By.NAME,'g_name')))
    ActionChains(driver).send_keys_to_element(title, data['title']).perform()

    #위치
    iframe = WebDriverWait(driver,60).until(EC.presence_of_all_elements_located((By.TAG_NAME,'iframe')))
    driver.switch_to.frame(iframe[0])
    locate = WebDriverWait(driver,60).until(EC.presence_of_element_located((By.ID,'gym_keyword')))
    add=""
    str_tmp=data['address'][0].split(" ")
    for idx in range(0,4 if len(str_tmp)>4 else len(str_tmp)):
        add=add+str_tmp[idx]+" "
    ActionChains(driver).send_keys_to_element(locate, add).perform()
    ActionChains(driver).click(driver.find_element_by_class_name('btn_search')).perform()
    tmp_tag=WebDriverWait(driver,60).until(EC.presence_of_element_located((By.ID,'placesList'))).find_elements_by_tag_name('li')
    if len(tmp_tag)!=0:
        tf=False
        pg=driver.find_elements_by_css_selector('#pagination>a')
        pg_size=len(pg)
        for j in range(0,pg_size):
            pg = driver.find_elements_by_css_selector('#pagination>a')
            ActionChains(driver).click(pg[j]).perform()
            time.sleep(1)
            tags = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'h5')))
            stop=False
            for k in range(0,len(tags)):
                if tags[k].text.find(data['title'])!=-1:
                    tf=True
                    ActionChains(driver).click(tags[k]).perform()
                    stop=True
                    break;
            if stop:
                break;
        if not tf:
            ActionChains(driver).click(tmp_tag[0]).perform()
    driver.switch_to.default_content()
    time.sleep(1)

    #세부내용 + 가격
    texts = ""
    price_size = len(data['prices'])
    if price_size != 0:
        for ttm in data['prices']:
            tmp = ttm.split('\n')
            texts = texts + tmp[1] + " : " + tmp[0] + "\n"
        texts = texts + "\n\n"
    if len(data['details']) != 0:
        texts = texts + data['details'][0]
    #종목
    type_add = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'btn_add')))
    ActionChains(driver).click(type_add[1]).perform()
    type_cnt=1
    index=1
    if len(texts)!=0:
        pressed_details=texts.replace(" ","")
        for tmp in correct:
            k=tmp.replace(" ","")
            if pressed_details.find(k) != -1:
                if type_cnt==9:
                    break
                type_add = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'btn_add')))
                ActionChains(driver).click(type_add[1]).perform()
                type_cnt=type_cnt+1
                scroll = driver.find_element_by_name('g_category[' + str(index) + ']').find_elements_by_tag_name('option')
                for j in range(0, len(scroll)):
                    if scroll[j].text==tmp:
                        driver.execute_script("arguments[0].setAttribute('selected','')", scroll[j])
                        break
                index = index + 1

    time.sleep(1)
    #이용시간
    use_time1 = WebDriverWait(driver,60).until(EC.presence_of_element_located((By.NAME,'use_hours_0')))
    use_time2 = WebDriverWait(driver,60).until(EC.presence_of_element_located((By.NAME,'use_hours_1')))
    use_time3 = WebDriverWait(driver,60).until(EC.presence_of_element_located((By.NAME,'use_hours_2')))
    mon_text = ""
    sat_text = ""
    hol_text = ""
    for i in range(0,len(data['times'])):
        temp=data['times'][i].split()
        if temp[0]=='평일':
            mon_text=mon_text+temp[1]
        elif temp[1]=='휴관' or temp[1]=='휴무':
            if hol_text!="":
                hol_text=hol_text+" / "
            hol_text=hol_text+temp[0]
        else:
            if sat_text!="":
                sat_text=sat_text+" / "
            sat_text=sat_text+temp[0]+" : "+temp[1]
    if mon_text=="":
        mon_text="X"
    if sat_text=="":
        sat_text="X"
    if hol_text=="":
        hol_text="X"
    ActionChains(driver).send_keys_to_element(use_time1, mon_text).perform()
    ActionChains(driver).send_keys_to_element(use_time2, sat_text).perform()
    ActionChains(driver).send_keys_to_element(use_time3, hol_text).perform()

    #전화번호
    if len(data['phone'])!=0:
        phone = WebDriverWait(driver,60).until(EC.presence_of_element_located((By.ID,'g_hp')))
        ActionChains(driver).send_keys_to_element(phone, data['phone'][0]).perform()
    time.sleep(1)
    #세부내용
    driver.switch_to.frame(iframe[1])
    detail = WebDriverWait(driver,60).until(EC.presence_of_element_located((By.CLASS_NAME,'se2_input_wysiwyg')))
    if texts=="":
        texts="X"
    ActionChains(driver).send_keys_to_element(detail, texts).perform()
    driver.switch_to.default_content()
    time.sleep(3)



def add_pic_box(cnt):
    tag = WebDriverWait(driver,60).until(EC.presence_of_all_elements_located((By.TAG_NAME,'td')))
    pic_cnt = 1
    tt=WebDriverWait(driver,60).until(EC.presence_of_element_located((By.NAME,'cnt_file')))
    if cnt>20:
        cnt=20
    driver.execute_script("arguments[0].setAttribute('value',arguments[1])", tt, cnt)
    str1 = '<div class="filebox wh1 multi">' \
           + '<input class="upload-name" value="파일선택" disabled="disabled">' \
           + '<label for="reg_file' + str(pic_cnt) + '" class="reg_file"></label>' \
    +'<input type="file" name="bf_file[]" id="reg_file'+str(pic_cnt)+'" class="upload-hidden" onchange="upload_preview(this);">'\
           + '<button type="button" class="del" title="삭제"></button>' \
           + '</div> '
    driver.execute_script("arguments[0].insertAdjacentHTML('beforeend',arguments[1])", tag[0], str1)

def click_submit():
    submit_btn=WebDriverWait(driver,60).until(EC.presence_of_element_located((By.CLASS_NAME,'btn_submit')))
    ActionChains(driver).click(submit_btn).perform()

#keyword = "대전광역시 헬스장"
keyword = "스포애니 강남역1호점"
fun1(keyword)
# get_ids(ui_data['KEYWORD'])
#큰사진 =37427547,36947326
# sample_id = ['31663836','34228730']
# for a in sample_id:
#     URL = "https://map.naver.com/local/siteview.nhn?code=" + a
#     driver.get(URL)
#     time.sleep(1)
#     make_data()

show=0

# for a in range(160,len(id_list)):
#     URL = "https://map.naver.com/local/siteview.nhn?code=" + id_list[a]
#     driver.get(URL)
#     time.sleep(1)
#     make_data()
#     show=show+1
#     if show%10==0:
#         print(show)

print("searched data : "+str(len(data_list)))
print(data_list)
# gym site inesert

site="http://dmonster874.cafe24.com/bbs/login.php?url=http%3A%2F%2Fdmonster874.cafe24.com%2F"
options = Options()
options.add_argument("--start-maximized")
driver=webdriver.Chrome(os.getcwd()+'/chromedriver',options=options)
driver.set_page_load_timeout(100)
driver.get(site)
driver.implicitly_wait(3)

id_box=driver.find_element_by_id('login_id')
pw_box=driver.find_element_by_id('login_pw')
login_btn=driver.find_element_by_class_name('btn_submit')
ActionChains(driver).send_keys_to_element(id_box,'manager3').send_keys_to_element(pw_box,'manager3').click(login_btn).perform()
admin_btn=driver.find_elements_by_tag_name('a')
ActionChains(driver).click(admin_btn[3]).perform()
driver.implicitly_wait(3)

show2=0
for abc in range(0,len(data_list)):
    print(data_list[abc]['title'])
    insert_data(data_list[abc])
    click_submit()
    try:
        WebDriverWait(driver, 100).until(EC.alert_is_present(),'Timed out waiting for PA creation ' +'confirmation popup to appear.')
    except:
        print("time out !!")
        driver.refresh();
        abc=abc-1
        out=True
        continue
    art = driver.switch_to.alert
    art.accept()
    driver.switch_to.default_content()
    time.sleep(2)
    print(show2)
    show2=show2+1

##파일저장
# url="http://ldb.phinf.naver.net/20160322_64/1458654453155zVjxg_JPEG/176272627752929_0.jpeg"
# myfile = requests.get(url)
# open('/home/jung/다운로드/abc.jpeg', 'wb').write(myfile.content)
