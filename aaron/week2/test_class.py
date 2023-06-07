from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class test_process:


    #初始化dirver設定
    def __init__(self):
        
        option = Options()

        option.add_experimental_option('detach', True)

        driver = webdriver.Chrome(options=option)

        self.driver = driver


    #設定語系、輸入帳號、密碼
    def login(self, url, lang_set, account, password):

        self.driver.get(url)

        lang_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'div[class="el-dropdown-link el-input el-input__inner el-dropdown-selfdefine"]')))

        login_info = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'input[class="el-input__inner"]')))

        login_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button[class="el-button submit el-button--default"]')))

        lang_btn.click()

        lang_ul = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'ul[class="el-dropdown-menu el-popper lang-menu"]')))

        lang_li = lang_ul.find_elements(By.TAG_NAME, 'li')

        for lang in lang_li:

            if lang.text == lang_set:

                lang.click()

        login_info[0].click()

        login_info[0].send_keys(account)

        login_info[1].click()

        login_info[1].send_keys(password)

        login_btn.click()


    #切換頁面
    def switch_page(self, page):
        
        if WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "operator-name"))):

            search_bar = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "el-input__inner")))

            search_bar.click()

            search_bar.send_keys(page)

            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, page))).click()



    def search_by_round(self, lobby_set, search_type_set, wagersid):

        #切換至iframe
        iframe = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "iframe-item")))

        self.driver.switch_to.frame(iframe)

        #選擇遊戲平台
        lobby_ul = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'ul[class="nav nav-tabs"]')))
            
        lobby_li = lobby_ul.find_elements(By.TAG_NAME, 'li')

        for lobby in lobby_li:

            if lobby.text == lobby_set:

                lobby.click()

                break


        search_type_group = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div[class="form-group"]')))

        search_type_btn = search_type_group.find_element(By.CSS_SELECTOR, 'a[class="ui-button ui-widget ui-state-default ui-button-icon-only custom-combobox-toggle ui-corner-right"]')

        wagersid_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'input[id="wagersid"]')))

        serach_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button[class="btn btn-info"]')))

        title_list = []

        info_list = []
        

        #選擇搜尋方式
        search_type_btn.click()

        search_type_ul = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'ul[class="ui-autocomplete ui-front ui-menu ui-widget ui-widget-content"]')))
            
        search_type_li = search_type_ul.find_elements(By.TAG_NAME, 'li')


        for search_type in search_type_li:

            if search_type.text == search_type_set:
                    
                search_type.click()

                break

        #輸入搜尋資料並送出
        wagersid_input.click()

        wagersid_input.send_keys(wagersid)

        serach_btn.click()


        #抓取結果印出
        search_result = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'table[class="table table-hover text-middle table-bordered"]')))

        result_title = search_result.find_elements(By.TAG_NAME, 'th')

        result_info = search_result.find_elements(By.TAG_NAME, 'td')


        for title in result_title:

            title_list.append(title.text)

        for info in result_info:

            info_list.append(info.text)

        print(dict(zip(title_list, info_list)))


    def finsh(self):
        self.driver.quit()


