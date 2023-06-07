class SearchDict:
    def search(self, dict1, count=1, keyword=""):
        dict2 = {}
        keyword += input("請輸入第 " + str(count) + " 個關鍵字").lower()
        for key in dict1:
            if keyword[count - 1] == key[count - 1]:
                dict2[key] = dict1[key]
        if len(dict2) == 0:
            return print("找不到關鍵字對應的值")
        elif len(dict2) == 1:
            return print("對應的值為：" + list(dict2.values())[0])
        else:
            count += 1
            return self.search(dict2, count, keyword)


if __name__ == "__main__":
    print("原檔案測試")
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
    test = SearchDict()
    test.search(dict1=all_month)
