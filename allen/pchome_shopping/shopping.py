from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from openpyxl import Workbook
import datetime
import time


def pchome_search(keywords, max_amount=100):
    try:
        # 定義search方法，keyword為搜尋的關鍵字；max_amount為預計爬取的資料數量；save_xlsx為是否儲存成xlsx

        with open("./wd.txt", "r", encoding="utf-8") as f:
            path = f.readlines()[2].replace("\n", "").replace("\\", "/")
        # 以唯讀的方式開啟wd.txt檔案，去取得第三行的文字(webdriver的路徑)，並將路徑的\n替換成空白；\替換成/，python才有辦法辨識

        opts = webdriver.ChromeOptions()
        # 建立一個webdriver.ChromeOptions的物件，用於設定自動化瀏覽器的參數

        prefs = {"profile.default_content_setting_values.notifications": 1}
        # 網頁的隱私權和安全性設定-網站設定-通知
        # value為 1 允許傳送通知； 2 禁止傳送通知(因pchome會跳出詢問視窗，這邊直接設定好可以避免出現彈跳視窗)
        prefs["profile.managed_default_content_settings.images"] = 2
        # 控制瀏覽器是否要載入圖片
        # value為 1 允許載入圖片； 2 禁止載入圖片； 3 使用瀏覽器預設值
        opts.add_experimental_option("prefs", prefs)
        # 加入實驗性選項

        # opts.add_experimental_option("excludeSwitches", ["enable-logging"])
        # 因pchome會一直噴憑證錯誤，加上此訊息可以隱藏錯誤訊息
        opts.add_experimental_option("detach", True)
        # 設定程式運行結束後，不要自動關閉webdriver(使用quit()後才關閉)

        driver = webdriver.Chrome(path, chrome_options=opts)
        # 使用webdrive啟動Chrome，並帶入webdriver路徑、chorme_options的參數

        url = "https://24h.pchome.com.tw/"
        # pchome的網址
        driver.get(url)
        # 前往指定網址url，這邊是前往pchome

        search = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,'//input[@type="text" and @class="l-header__siteSearchInput"]')))
        # 等待"搜尋框"出現，再將輸入框元素位置存在search
        search.clear()
        # 清除search"搜尋框"的文字
        search.send_keys(keywords)
        # 將keyword輸入至"搜尋框"
        search.send_keys(Keys.RETURN)
        # 按下enter進行搜尋

        prod_amount = int(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@id="SearchInfo"]/span[@class="value"]'))).text)
        # 等待"共找到 xxx 筆"的資料出現，並取得搜尋到的總商品數量xxx
        if prod_amount == 0:
            driver.quit()
            print(f"找不到【{keywords}】的資料")
            return {}
            # 如果搜尋的商品數量為 0 ，則關閉瀏覽器，提示"找不到【xxx】的資料，結束方法並回傳空的字典

        try:
            all_items = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//dd//li[@id="cate_D" and @class="expanded"]/a')))
            # 等待"24h購物"的按鈕出現
            all_items.click()
            # 點擊"24h購物"按鈕(未點擊的話，網頁的商品數量會有問題)
        except:
            driver.quit()
            print('出事了阿北，找不到"24h購物"的按鈕')
            return None
            # 找不到"24h購物"的按鈕時，中斷程式並提示

        prod_amount = int(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@id="SearchInfo"]/span[@class="value"]'))).text)
        # 等待"共找到 xxx 筆"的資料出現，並取得搜尋到的總商品數量xxx
        get_prod_amount = 0
        # 建立get_prod_amount變數，並設定為 0 ，用於計算目前瀏覽器顯示的商品數量
        break_count = max_amount // 20 + 3
        # 建break_count變數，並設定為預計爬取的資料數量除20取整數，再加5，用於避免下方取資料的時候陷入無窮迴圈
        # 因瀏覽器捲動到最底部，每次最多顯示20筆商品
        while get_prod_amount != prod_amount and get_prod_amount < max_amount:
            # 目前頁面顯示的商品數量與搜尋到的總商品數量不同，且目前頁面顯示的商品數量小於預計爬取的資料數量
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # 使用JS語法，讓網頁模擬捲動到最底部，使瀏覽器顯示更多商品
            get_prod_amount = len(driver.find_elements(By.XPATH, '//h5[@class="prod_name"]/a'))
            # 取得目前瀏覽器內，顯示的商品數量
            print("搜尋到的總商品數量為", prod_amount)
            print("目前頁面顯示的商品數量為", get_prod_amount)
            # 印出相關資訊來檢視目前進度
            break_count -= 1
            # 每跑一次迴圈，break_count減1
            time.sleep(2)
            # 等待瀏覽器載入更多商品

            if break_count <= 0:
                print("又出事了阿北，迴圈一直跑，煞不住，爬取的資料數量有異常")
                break
            # 當break_count小於等於0時，表示迴圈跑的次數過多，中斷程式

        if max_amount > get_prod_amount:
            max_amount = get_prod_amount
        # 如果預計爬取的資料數量，大於目前瀏覽器顯示的商品數量，把max_amount設定為get_prod_amount，後續是用來當做最後抓取的數量

        prod_list = driver.find_elements(By.XPATH, '//h5[@class="prod_name"]/a')
        prod_nick = driver.find_elements(By.XPATH, '//span[@class="nick"]')
        prod_label = driver.find_elements(By.XPATH,'//ul[contains(@id, "marketing_") and @class="tag_box s_marketing"]')
        price_list = driver.find_elements(By.XPATH,'//span[@class="price"]/span[contains(@id, "price_") and @class="value"]')
        prod_state = driver.find_elements(By.XPATH, '//ul[@class="fieldset_box"]//button')
        prod_url = driver.find_elements(By.XPATH, '//h5[@class="prod_name"]/a[contains(@href, "")]')
        # 爬取目前瀏覽器所有"產品名稱", "產品資訊", "標籤", "價格", "狀態", "商品網址"的列表資料

        prod_infos = {}
        # 建立空字典，用於存放商品資訊

        for i in range(max_amount):
            prod = prod_list[i].text
            nick = prod_nick[i].text
            label = prod_label[i].text
            price = price_list[i].text
            state = prod_state[i].text
            if state == "加入購物車" or state == "立即訂購":
                state = "目前可以購買!"
            url = prod_url[i].get_attribute("href")

            list1 = [prod, nick, label, price, state, url]
            prod_infos[i + 1] = list1
            # 取得個列表裡，每一個"產品名稱", "產品資訊", "標籤", "價格", "狀態", "商品網址"的資料，並放到新列表中
            # 只取max_amount個
            # 把商品資訊方在列表內，並存到prod_infos字典中
            # prod_infos內容為{1:["產品名稱",...], 2:["產品名稱",...], ...}

        driver.quit()
        # 離開自動化瀏覽器

        print(f"已經從pchome爬取 {str(max_amount)} 筆【{keywords}】的資料")
        # 印出爬蟲的結果

        return prod_infos
        # 回傳商品資訊(字典)
    except:
        driver.quit()
        print("爬取資料有問題...")
        return None


def save_xlsx(keywords, prod_infos):
    # 將檔案存成excel
    try:
        wb = Workbook()
        ws = wb.active
        ws.title = keywords
        ws.append(["項次", "產品名稱", "產品資訊", "標籤", "價格", "狀態", "商品網址"])
        for info in prod_infos:
            prod_infos[info].insert(0, info)
            ws.append(prod_infos[info])

        now = datetime.datetime.now().strftime("(%Y-%m-%d %H-%M-%S)")
        file_name = keywords + " " + now + ".xlsx"
        wb.save(file_name)
        print(f"已將資料存成xlsx檔，檔名為：{file_name}")
        # 將爬蟲結果存成xlsx檔
    except:
        print("存檔的時候出現了問題...")


if __name__ == "__main__":
    try:
        choice = input("A：使用預設展示程式\nB：自己輸入關鍵字來搜尋\n請輸入A或B：").upper()
        if choice == "A":
            keywords = "超級瑪莉"
            max_amount = 100
        elif choice == "B":
            keywords = input("請輸入要搜尋的關鍵字：")
            max_amount = int(input("請輸入最大搜尋筆數："))
        else:
            print("輸入錯了...")

        result = pchome_search(keywords, max_amount)
        if result != None and len(result) > 0:
            print(f"\n\n搜尋結果如下：\n==========\n{result}\n==========\n")
            save_xlsx(keywords, result)
    except Exception as e:
        print("怪怪的")
        print(e)
