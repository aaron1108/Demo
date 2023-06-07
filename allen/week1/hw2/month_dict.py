# 輸入月的第一個英文字母判斷是幾月 如果第一個字母一樣就判斷第二個字母 這裡用def 和字典檔的形式去做
# 這兩題都要用class和def 以及 if name == '__main__’:去做
from search import SearchDict

all_month = {
        "jan": "January",
        "feb": "February",
        "mar": "March",
        "apr": "April",
        "jun": "June",
        "jul": "July",
        "aug": "August",
        "sep": "September",
        "oct": "October",
        "nov": "November",
        "dec": "December",
        }

s = SearchDict()
s.search(dict1=all_month)
